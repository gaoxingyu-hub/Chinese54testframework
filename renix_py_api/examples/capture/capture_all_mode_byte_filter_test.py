from renix_py_api.renix import *
import time
initialize(log_level=logging.INFO)


def wait_port_online(port, times=10):
    port.set_force_auto_sync(True)
    while times:
        if port.Online:
            return True
        else:
            times -= 1
            time.sleep(1)
    else:
        return False


def create_ports(sys_entry, locations):
    renix_info('Create ports with locations: '.format(locations))
    port1 = Port(upper=sys_entry, Location=locations[0])
    port2 = Port(upper=sys_entry, Location=locations[1])

    assert port1.handle
    assert port2.handle

    bring_port_online_cmd = BringPortsOnlineCommand(PortList=[port1.handle, port2.handle])
    bring_port_online_cmd.execute()
    if not wait_port_online(port1):
        raise Exception('bring online port({}) failed'.format(port1.handle))
    if not wait_port_online(port2):
        raise Exception('bring online port({}) failed'.format(port2.handle))

    return port1, port2


def create_stream(port, packet_length=128):
    renix_info('port({}) create streams'.format(port.Location))
    stream = StreamTemplate(upper=port)
    assert stream.handle

    create_stream_header_cmd = CreateHeaderCommand(stream.handle, ['Ethernet.ethernetII', 'IPv4.ipv4'])
    create_stream_header_cmd.execute()
    if len(create_stream_header_cmd.HeaderNames) != 2:
        raise Exception('{} create EthernetII and IPv4 header failed'.format(stream.handle))
    stream.FixedLength = packet_length

    return stream


def get_capture(port):
    renix_info('port({}) get captures'.format(port.Location))
    capture_cfgs = port.get_relatives('lower', relative_name=CaptureConfig.cls_name())
    if not capture_cfgs or len(capture_cfgs) <= 0:
        raise Exception('No capture config on port: {}'.format(port.handle))
    return capture_cfgs[0]


if __name__ == '__main__':
    renix_info('Capture all mode with Byte filter mode test begin')

    # v6004c port
    # port_location = ('//10.1.5.16/1/1', '//10.1.5.16/1/2')

    # v6008c v6008m v6016c port
    # port_location = ('//10.1.5.10/1/5', '//10.1.5.10/1/6')

    # v8004f v8008f port
    port_location = ('//10.1.5.10/2/1', '//10.1.5.10/2/2')

    # v8008M v8008c port
    # port_location = ('//10.1.5.15/1/1', '//10.1.5.15/1/2')

    # v2-10G port
    # port_location = ('//10.1.6.199/2/1', '//10.1.6.199/2/2')

    # v98-100G port
    # port_location = ('//10.1.6.149/2/1', '//10.1.6.149/2/2')

    # x8 port
    # port_location = ('//10.1.5.12/2/1', '//10.1.5.12/2/2')

    # x6 port
    # port_location = ('//10.1.5.12/1/1', '//10.1.5.12/1/2')

    # create ports
    sys_entry = get_sys_entry()
    port1, port2 = create_ports(sys_entry, port_location)

    stream_port_cfgs = port1.get_children(StreamPortConfig.cls_name())
    assert stream_port_cfgs
    stream_port_cfg = stream_port_cfgs[0]
    assert stream_port_cfg.handle
    stream_port_cfg.edit(TransmitMode=EnumTransmitMode.BURST)
    stream_port_burst_cfgs = stream_port_cfg.get_children(BurstTransmitConfig.cls_name())
    stream_port_burst_cfg = stream_port_burst_cfgs[0]
    stream_port_burst_cfg.edit(FramePerBurst=1000)

    # create streams
    stream = create_stream(port1)
    modifier = ['ipv4_1.id.XetModifier.Type=Increment', 'ipv4_1.id.XetModifier.Start=123',
                'ipv4_1.id.XetModifier.Step=1', 'ipv4_1.id.XetModifier.Count=1000']
    update_header_cmd = UpdateHeaderCommand(stream.handle, modifier)
    update_header_cmd.execute()

    # get capture and set capture byte conditions
    cap_cfg = get_capture(port2)
    cap_cfg.FilterMode = EnumFilterMode.BYTE
    byte_filter = CaptureByteFilter(upper=cap_cfg)
    mask = [0xff, 0xff]
    data = [0x00, 0x7D]
    offset = 18
    byte_condition = CaptureByteCondition(upper=byte_filter, Mask=mask, Data=data, Offset=offset)

    # subscribe statistic
    result_view1 = ResultView(upper=sys_entry, DataClassName=StreamBlockRxStats.cls_name())
    result_query1 = ResultQuery(upper=result_view1)
    subcribe_result_cmd = SubscribeResultCommand(ResultViewHandles=[result_view1.handle])
    subcribe_result_cmd.execute()

    # start capture and stream
    start_capture_cmd = StartCaptureCommand(CaptureConfigs=[cap_cfg.handle])
    start_capture_cmd.execute()

    start_stream_cmd = StartStreamCommand(StreamList=[stream.handle])
    start_stream_cmd.execute()
    time.sleep(15)

    # stop stream and capture
    stop_stream_cmd = StopStreamCommand(StreamList=[stream.handle])
    stop_stream_cmd.execute()

    stop_capture_cmd = StopCaptureCommand(CaptureConfigs=[cap_cfg.handle])
    stop_capture_cmd.execute()

    statistics = result_query1.get_relatives('lower', StreamBlockRxStats.cls_name())
    if len(statistics) <= 0:
        raise Exception('Get stream block rx statistic failed.')
    stream1_statistic = statistics[0]

    if stream1_statistic.RxStreamFrames == 0:
        raise Exception('port{} receive no packets'.format(port2.Location))

    # download capture
    cap_cfg.get()
    if cap_cfg.CapturedPacketCount == 0:
        raise Exception('Capture packet count is 0')

    pcap_dir = os.path.normpath(os.path.join(os.path.dirname(sys.argv[0]), 'logs'))
    download_capture_cmd = DownloadCaptureDataCommand(FileDir=pcap_dir, FileName='CaptureAllModeByteFilter.pcap',
                                                      CaptureConfigs=[cap_cfg.handle])
    download_capture_cmd.execute()

    # waiting for download finish
    cap_cfg.set_force_auto_sync(True)
    while True:
        if cap_cfg.CaptureState == EnumCaptureState.IDLE and cap_cfg.CapturedPacketCount == cap_cfg.DownloadedPacketCount:
            renix_info('Download packets finish, downloaded count: {}'.format(cap_cfg.DownloadedPacketCount))
            break
        else:
            time.sleep(1)
    renix_info('Capture packet count is : {}'.format(cap_cfg.DownloadedPacketCount))
    for i in range(cap_cfg.DownloadedPacketCount):
        get_index_cmd = GetCaptureDataByIndexCommand(cap_cfg.handle, i + 1)
        get_index_cmd.execute()
        cap_data = get_index_cmd.Data.strip().split()
        if len(cap_data) < 20 or cap_data[18: 20] != ['00', '7D']:
            raise Exception('Capture byte filter failed in ALL mode')

    renix_info('Capture byte filter test in all mode success')