"""
Auto-generated File 
Create Time: 2019-12-27 02:33:26
"""
from .ROMEnum_Autogen import *
from renix_py_api.renix_common_api import *
from renix_py_api import rom_manager
from .ROMCommand_Autogen import ROMCommand


@rom_manager.rom
class Dhcpv6ClientCommand(ROMCommand):
    def __init__(self, Dhcpv6Clients=None, **kwargs):
        self._Dhcpv6Clients = Dhcpv6Clients  # DHCPv6/PD Client Protocol Configs

        properties = kwargs.copy()
        if Dhcpv6Clients is not None:
            properties['Dhcpv6Clients'] = Dhcpv6Clients

        # call base class function, and it will send message to renix server to create a class.
        super(Dhcpv6ClientCommand, self).__init__(**properties)

    @property
    def Dhcpv6Clients(self):
        """
        get the value of property _Dhcpv6Clients
        """
        return self._Dhcpv6Clients

    @Dhcpv6Clients.setter
    def Dhcpv6Clients(self, value):
        self._Dhcpv6Clients = value

    def _set_dhcpv6clients_with_str(self, value):
        tmp_value = value.strip()
        if tmp_value.startswith('{'):
            tmp_value = tmp_value[1:-1]
        self._Dhcpv6Clients = tmp_value.split()

