from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import QMessageBox
from common.config import TestModuleConfigNew, SystemConfig
from common.th_thread_model import ThThreadTimerUpdateTestTime
from modules.info.testInfo import TestInfo
import os
import frozen_dir
from common.logConfig import Logger
import time
from modules.VHF_radio.TEST1 import DialogTest1
from modules.VHF_radio.VHF_radio_CONSTANT import ModuleConstants
from modules.VHF_radio.TEST2 import DialogTest2
from common.info import Constants
from modules.VHF_radio.TEST6 import DialogTest6
from modules.VHF_radio.TEST7 import DialogTest7
from modules.VHF_radio.TEST7point2 import DialogTest7point2
from modules.VHF_radio.TEST7point5 import DialogTest7point5
from modules.VHF_radio.TEST8 import DialogTest8
from modules.VHF_radio.TEST9 import DialogTest9
from modules.VHF_radio.TEST10_1 import DialogTest10_1
from modules.VHF_radio.TEST10_2 import DialogTest10_2
from modules.VHF_radio.TEST11 import DialogTest11
from modules.VHF_radio.TEST10point2_1 import DialogTest10point2_1
from modules.VHF_radio.TEST10point2_2 import DialogTest10point2_2
from modules.VHF_radio.TEST10point6_2 import DialogTest10point6_2
from modules.VHF_radio.TEST12_1 import DialogTest12_1
from modules.VHF_radio.TEST12_2 import DialogTest12_2
from modules.VHF_radio.TEST17 import DialogTest17
from modules.VHF_radio.TEST20_1 import DialogTest20_1
from modules.VHF_radio.TEST22_2 import DialogTest22_2
from modules.VHF_radio.TEST25 import DialogTest25
from modules.VHF_radio.TEST28 import DialogTest28
from database.data_storage import ThTestResultsStorage
from database.test_results_model import TestResultBase
from modules.VHF_radio.Ui_VHF_radio_MAIN import Ui_Dialog
from datetime import datetime

from PyQt5.QtWidgets import QApplication

SETUP_DIR = frozen_dir.app_path()
logger = Logger.module_logger("VHF_radio")
#
class VHFradioMain(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    signalTitle = pyqtSignal(str)
    signalStatus = pyqtSignal(str)
    debug_model = True
    start_test_flag = False

    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(VHFradioMain, self).__init__(parent)
        self.setupUi(self)

        self.current_test_step = 0

        self.config_file_path = os.path.join(
            SETUP_DIR, "conf", "vhf_radio.json")
        self.system_config_file_path = os.path.join(
            SETUP_DIR, "conf", "system.json")
        self.test_config = TestModuleConfigNew(self.config_file_path)
        self.pic_file_path = os.path.join(
            SETUP_DIR, "imgs", "vhf_radio")

        self.system_config = SystemConfig(self.system_config_file_path)
        self.steps2Name = self.system_config.step2name

        self.test_time_update_obj = ThThreadTimerUpdateTestTime()

        self.selected_test_cases = None  # 用来记录选中的测试项目
        self.test_cases_records = None  # 用来记录测试项目的执行测试的进度
        self.current_test_case = None  # 记录当前执行的test case

        self.last_test_case_status = ""
        self.last_test_case_result = ""

        # init tree widget for test cases 树形控件

        self.treeWidget.clear()
        parent = QTreeWidgetItem(self.treeWidget)
        parent.setText(0, self.test_config.title)
        parent.setFlags(parent.flags() | Qt.ItemIsTristate | Qt.ItemIsUserCheckable)

        # insert test resource data
        self.tableWidget_test_resource.setRowCount(len(self.test_config.test_source))
        # load test resource
        for x in range(len(self.test_config.test_source)):
            item = QTableWidgetItem(str(x + 1))
            self.tableWidget_test_resource.setItem(x, 0, item)
            # name
            item = QTableWidgetItem(str(self.test_config.test_source[x]["name"]))
            self.tableWidget_test_resource.setItem(x, 1, item)
            # type
            item = QTableWidgetItem(str(self.test_config.test_source[x]["type"]))
            self.tableWidget_test_resource.setItem(x, 2, item)
            # number
            item = QTableWidgetItem(str(self.test_config.test_source[x]["number"]))
            self.tableWidget_test_resource.setItem(x, 3, item)
            # count
            item = QTableWidgetItem(str(self.test_config.test_source[x]["count"]))
            self.tableWidget_test_resource.setItem(x, 4, item)
            # set font center
            for a in range(0, 5):
                self.tableWidget_test_resource.item(x, a).setTextAlignment(Qt.AlignCenter)

            # set vertical header center
            item = QTableWidgetItem(str(x + 1))
            self.tableWidget_test_resource.setVerticalHeaderItem(x, item)
            self.tableWidget_test_resource.verticalHeaderItem(x).setTextAlignment(Qt.AlignCenter)

        for x in range(len(self.test_config.test_case)):
            child = QTreeWidgetItem(parent)
            child.setFlags(child.flags() | Qt.ItemIsUserCheckable)
            child.setText(0, self.test_config.test_case_detail[x]["title"])
            child.setCheckState(0, Qt.Unchecked)
        # table widget 自适应
        self.tableWidget_test_resource.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.tableWidget_test_results.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        # remove grid
        self.tableWidget_test_resource.setShowGrid(False)
        self.tableWidget_test_results.setShowGrid(False)
        # set alter color
        self.tableWidget_test_resource.setAlternatingRowColors(True)
        self.tableWidget_test_results.setAlternatingRowColors(True)
        self.tableWidget_test_resource.setColumnWidth(0, 30)
        self.tableWidget_test_resource.setColumnWidth(2, 60)
        self.tableWidget_test_resource.setColumnWidth(3, 150)
        self.tableWidget_test_results.setColumnWidth(0, 30)
        self.tableWidget_test_results.setColumnWidth(1, 300)
        self.test_result = {}
        logger.info("VHF_radio inited")

    @pyqtSlot()
    def on_pushButton_start_clicked(self):
        """
        Slot documentation goes here.
        """
        self.selected_test_cases = self.get_checked_test_cases()

        if len(self.selected_test_cases) == 0:
            QMessageBox.warning(self, ModuleConstants.QMESSAGEBOX_WARN, ModuleConstants.QMESSAGEBOX_WARN_SELECTED_TEST)
            return

        self.test_cases_records = {}
        for item in self.selected_test_cases:
            for x in range(len(self.test_config.test_case)):
                if item in self.test_config.test_case_detail[x]["title"]:
                    temp = {}
                    temp["current"] = 1
                    temp["max"] = len(self.test_config.test_case_detail[x]["steps"])
                    self.test_cases_records[item] = temp

        self.current_test_step = 1
        self.start_test_flag = True
        self.start_caculate_test_duration()
        self.test_process_control(ModuleConstants.PROCESS_CONTROL_NEXT)
        logger.info("ecom ns1 test process start")

    @pyqtSlot()
    def on_pushButton_restart_clicked(self):
        """
        Slot documentation goes here.
        """
        if not self.debug_model:
            test = TestInfo()
            test.setWindowTitle(self.test_config.title)
            if test.exec_():
                if test.flag == -1:
                    QMessageBox.warning(self, ModuleConstants.QMESSAGEBOX_WARN,
                                        ModuleConstants.QMESSAGEBOX_WARN_INPUT_PARAMETER_NOT_ENOUGH)
            else:
                QMessageBox.warning(self, ModuleConstants.QMESSAGEBOX_WARN,
                                    ModuleConstants.QMESSAGEBOX_WARN_INPUT_PARAMETER_NOT_ENOUGH)
            self.current_test_step = 0
        else:
            self.current_test_step = 1
        self.test_process_control(ModuleConstants.PROCESS_CONTROL_NEXT)
        self.start_caculate_test_duration()
        logger.info("ecom ns1 test process restart")

    @pyqtSlot()
    def on_pushButton_close_clicked(self):
        """
        Slot documentation goes here.
        """
        self.signalTitle.emit("close")
        self.close()
        logger.info("ecom_ns_1 test process close")
    #         return
    #进入测试进程
    def test_process_control(self, action,action2=""):
        if action == "next":
            for case, step in self.test_cases_records.items():
                if action2=='finish':
                    step["current"]=step["max"]+1
                if step["current"]>step["max"]:
                    continue
                    # get the test case detail parameters
                for x in range(len(self.test_config.test_case)):
                    if case in self.test_config.test_case_detail[x]["title"]:
                        temp_test_process = self.test_config.test_case_detail[x]["steps"][step["current"] - 1]
                        self.current_test_case = case
                        self.current_test_step_dialog = globals()[temp_test_process['module']]()
                        print(self.current_test_step_dialog)

                        if temp_test_process['module']=='DialogTest1' or temp_test_process['module'] == "DialogTest7point1":
                            self.current_test_step_dialog.signalFinish1.connect(self.deal_signal_test_next1)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], os.path.join(
                                    self.pic_file_path, temp_test_process['img']))

                        if temp_test_process['module'] == "DialogTest6" :
                           self.current_test_step_dialog.set_state(temp_test_process['state'])
                           self.current_test_step_dialog.initUi(self.test_config)
                           self.current_test_step_dialog.signalFinish1.connect(self.deal_signal_test_next1)
                           self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                   temp_test_process['contents'], os.path.join(
                                self.pic_file_path, temp_test_process['img']))

                        elif temp_test_process['module'] == "DialogTest2" :
                            self.current_test_step_dialog.set_state(temp_test_process['state'])
                            self.current_test_step_dialog.signalTest.connect(self.test_data_refresh)
                            self.current_test_step_dialog.signalPrint.connect(self.test_result_transform_and_storage)
                            self.current_test_step_dialog.signalFinish1.connect(self.deal_signal_test_next1)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], None)
                        elif temp_test_process['module'] == "DialogTest7" or temp_test_process['module']=='DialogTest17':
                            self.current_test_step_dialog.signalTest.connect(self.test_data_refresh)
                            self.current_test_step_dialog.signalFinish1.connect(self.deal_signal_test_next1)
                            self.current_test_step_dialog.signalFinish2.connect(self.deal_signal_test_next2)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], os.path.join(
                                    self.pic_file_path, temp_test_process['img']))
                        elif temp_test_process['module'] == "DialogTest9":
                            self.current_test_step_dialog.set_state(temp_test_process['state'])
                            self.current_test_step_dialog.signalTest.connect(self.test_data_refresh)
                            self.current_test_step_dialog.signalFinish1.connect(self.deal_signal_test_next1)
                            self.current_test_step_dialog.signalFinish2.connect(self.deal_signal_test_next2)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], os.path.join(
                                    self.pic_file_path, temp_test_process['img']))
                        elif temp_test_process['module'] == "DialogTest7point2":
                            self.current_test_step_dialog.set_state(temp_test_process['state'])
                            self.current_test_step_dialog.signalTest.connect(self.test_data_refresh)
                            self.current_test_step_dialog.signalPrint.connect(self.test_result_transform_and_storage)
                            self.current_test_step_dialog.signalFinish1.connect(
                                self.deal_signal_test_next1)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], os.path.join(
                                    self.pic_file_path, temp_test_process['img']))
                        elif temp_test_process['module'] == "DialogTest7point5":
                            self.current_test_step_dialog.set_state(temp_test_process['state'])
                            self.current_test_step_dialog.signalTest.connect(self.test_data_refresh)
                            self.current_test_step_dialog.signalPrint.connect(self.test_result_transform_and_storage)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], os.path.join(
                                    self.pic_file_path, temp_test_process['img']))
                        elif temp_test_process['module'] == "DialogTest8":
                            self.current_test_step_dialog.signalFinish1.connect(self.deal_signal_test_next6)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],temp_test_process['contents'],
                                    os.path.join(self.pic_file_path, temp_test_process['img']))

                        elif temp_test_process['module'] == "DialogTest10_1" :
                            self.current_test_step_dialog.signalFinish1.connect(self.deal_signal_test_up1)
                            self.current_test_step_dialog.signalFinish2.connect(self.deal_signal_test_next2)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], os.path.join(
                                    self.pic_file_path, temp_test_process['img']))
                        elif temp_test_process['module'] == "DialogTest10_2":
                            self.current_test_step_dialog.signalFinish1.connect(self.deal_signal_test_up2)
                            self.current_test_step_dialog.signalFinish2.connect(self.deal_signal_test_next2)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], os.path.join(
                                    self.pic_file_path, temp_test_process['img']))
                        elif temp_test_process['module'] == "DialogTest10point2_1":
                            self.current_test_step_dialog.set_state(temp_test_process['state'])
                            self.current_test_step_dialog.signalTest.connect(self.test_data_refresh)
                            self.current_test_step_dialog.signalPrint.connect(self.test_result_transform_and_storage)
                            self.current_test_step_dialog.signalFinish1.connect(self.deal_signal_test_up1)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], os.path.join(
                                    self.pic_file_path, temp_test_process['img']))
                        elif temp_test_process['module'] == "DialogTest10point2_2" :
                            self.current_test_step_dialog.signalFinish1.connect(self.deal_signal_test_up2)
                            self.current_test_step_dialog.signalFinish2.connect(self.deal_signal_test_next1)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], os.path.join(
                                    self.pic_file_path, temp_test_process['img']))
                        elif temp_test_process['module'] == "DialogTest10point6_2":
                            self.current_test_step_dialog.set_state(temp_test_process['state'])
                            self.current_test_step_dialog.signalTest.connect(self.test_data_refresh)
                            self.current_test_step_dialog.signalPrint.connect(self.test_result_transform_and_storage)
                            self.current_test_step_dialog.signalFinish1.connect(self.deal_signal_test_up2)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], os.path.join(
                                    self.pic_file_path, temp_test_process['img']))
                        elif temp_test_process['module'] == "DialogTest11":
                            self.current_test_step_dialog.signalTest.connect(self.test_data_refresh)
                            self.current_test_step_dialog.signalFinish1.connect(self.deal_signal_test_next10)
                            self.current_test_step_dialog.signalFinish2.connect(self.deal_signal_test_next11)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], os.path.join(
                                    self.pic_file_path, temp_test_process['img']))
                        elif temp_test_process['module'] == "DialogTest12_1":
                            self.current_test_step_dialog.signalFinish1.connect(self.deal_signal_test_up10)
                            self.current_test_step_dialog.signalFinish2.connect(self.deal_signal_test_next2)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], os.path.join(
                                    self.pic_file_path, temp_test_process['img']))
                        elif temp_test_process['module'] == "DialogTest12_2":
                            self.current_test_step_dialog.signalTest.connect(self.test_data_refresh)
                            self.current_test_step_dialog.signalPrint.connect(self.test_result_transform_and_storage)
                            self.current_test_step_dialog.signalFinish1.connect(self.deal_signal_test_up11)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], os.path.join(
                                    self.pic_file_path, temp_test_process['img']))
                        elif temp_test_process['module'] == "DialogTest20_1":
                            self.current_test_step_dialog.signalTest.connect(self.test_data_refresh)
                            self.current_test_step_dialog.signalFinish1.connect(self.deal_signal_test_up1)
                            self.current_test_step_dialog.signalFinish2.connect(self.deal_signal_test_next2)
                            self.current_test_step_dialog.signalPrint.connect(self.test_result_transform_and_storage)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], os.path.join(
                                    self.pic_file_path, temp_test_process['img']))
                        elif temp_test_process['module'] == "DialogTest25":
                            self.current_test_step_dialog.signalFinish1.connect(self.deal_signal_test_next2)
                            self.current_test_step_dialog.signalFinish2.connect(self.deal_signal_test_next1)
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], os.path.join(
                                    self.pic_file_path, temp_test_process['img']))
                        elif temp_test_process['module'] == "DialogTest28":
                            self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], os.path.join(
                                    self.pic_file_path, temp_test_process['img']))
                        self.current_test_step_dialog.exec_()
                        break

    def deal_signal_test_next1(self, flag, para):
        if self.current_test_step_dialog:
            self.current_test_step_dialog.action='next'
            self.current_test_step_dialog.close()
            if flag == 'finish_all':
                self.test_process_control('next', 'finish')
            else:
                self.test_cases_records[self.current_test_case]["current"] = \
                    self.test_cases_records[self.current_test_case]["current"] + 1
                time.sleep(0.1)
                self.test_process_control("next",None)

    def deal_signal_test_next2(self, flag, para):
        if self.current_test_step_dialog:
            self.current_test_step_dialog.action = 'next'
            self.current_test_step_dialog.close()
            if flag == 'finish_all':
                self.test_process_control('next', 'finish')
            else:
                self.test_cases_records[self.current_test_case]["current"] = \
                self.test_cases_records[self.current_test_case]["current"] + 2
                time.sleep(0.1)
                self.test_process_control("next", None)
#
    def deal_signal_test_next6(self, flag, para):
       if self.current_test_step_dialog:
            self.current_test_step_dialog.action = 'next'
            self.current_test_step_dialog.close()
            if flag == 'finish_all':
                self.test_process_control('next', 'finish')
            else:
                self.test_cases_records[self.current_test_case]["current"] = \
                self.test_cases_records[self.current_test_case]["current"] + 6
                time.sleep(0.1)
                self.test_process_control("next",None)
    def deal_signal_test_next10(self, flag, para):
       if self.current_test_step_dialog:
            self.current_test_step_dialog.action = 'next'
            self.current_test_step_dialog.close()
            if flag == 'finish_all':
                self.test_process_control('next', 'finish')
            else:
                self.test_cases_records[self.current_test_case]["current"] = \
                self.test_cases_records[self.current_test_case]["current"] + 10
                time.sleep(0.1)
                self.test_process_control("next",None)
    def deal_signal_test_next11(self, flag, para):
       if self.current_test_step_dialog:
            self.current_test_step_dialog.action = 'next'
            self.current_test_step_dialog.close()
            if flag == 'finish_all':
                self.test_process_control('next', 'finish')
            else:
                self.test_cases_records[self.current_test_case]["current"] = \
                self.test_cases_records[self.current_test_case]["current"] + 11
                time.sleep(0.1)
                self.test_process_control("next",None)

    def deal_signal_test_up1(self, flag, para):
        if self.current_test_step_dialog:
            self.current_test_step_dialog.action = 'next'
            self.current_test_step_dialog.close()
            if flag == 'finish_all':
                self.test_process_control('next', 'finish')
            else:
                self.test_cases_records[self.current_test_case]["current"] = \
                self.test_cases_records[self.current_test_case]["current"] - 1
                time.sleep(0.1)
                self.test_process_control("next", None)

    def deal_signal_test_up2(self, flag, para):
        if self.current_test_step_dialog:
            self.current_test_step_dialog.action = 'next'
            self.current_test_step_dialog.close()
            if flag == 'finish_all':
                self.test_process_control('next', 'finish')

            else:
                self.test_cases_records[self.current_test_case]["current"] = \
                self.test_cases_records[self.current_test_case]["current"] - 2
                time.sleep(0.1)
                self.test_process_control("next", None)

    def deal_signal_test_up10(self, flag, para):
        if self.current_test_step_dialog:
            self.current_test_step_dialog.action = 'next'
            self.current_test_step_dialog.close()
            if flag == 'finish_all':
                self.test_process_control('next', 'finish')
            else:
                self.test_cases_records[self.current_test_case]["current"] = \
                self.test_cases_records[self.current_test_case]["current"] - 10
                time.sleep(0.1)
                self.test_process_control("next", None)

    def deal_signal_test_up11(self, flag, para):
        if self.current_test_step_dialog:
            self.current_test_step_dialog.action = 'next'
            self.current_test_step_dialog.close()
            if flag == 'finish_all':
                self.test_process_control('next', 'finish')
            else:
                self.test_cases_records[self.current_test_case]["current"] = \
                self.test_cases_records[self.current_test_case]["current"] - 11
                time.sleep(0.1)
                self.test_process_control("next", None)
    def test_data_refresh(self,flag):
        self.current_test_step_dialog.action='next'
        self.table = self.tableWidget_test_results
        rowCount = self.table.rowCount()
        self.table.insertRow(rowCount)
        current_row = rowCount
        # the column number
        newItem = QTableWidgetItem(str(current_row+1))
        newItem.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.setItem(current_row, 0, newItem)

        mItem = self.current_test_step_dialog.test_result.test_item
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.setItem(current_row, 1, newItem)

        mItem = self.current_test_step_dialog.test_result.test_condition
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.setItem(current_row, 2, newItem)

        mItem = str(self.current_test_step_dialog.test_result.test_results)
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.setItem(current_row, 3, newItem)

        mItem = self.current_test_step_dialog.test_result.test_conclusion
        newItem = QTableWidgetItem(mItem)
        newItem.setTextAlignment(QtCore.Qt.AlignCenter)
        self.table.setItem(current_row, 4, newItem)
        time.sleep(0.1)



    def get_checked_test_cases(self):
        """
        get the tree widget checked test cases
        all the checked item are child nodes,not parent node
        :return:
        """
        selected_test_cases = []
        for item in self.treeWidget.findItems("", Qt.MatchContains | Qt.MatchRecursive):

            # excludes the parent node
            if item.parent() is None:
                continue

            # check the child node whether checked,if it had checked,
            # the checkState value greater than 0
            if item.checkState(0) > 0:
                selected_test_cases.append(item.text(0))
        return selected_test_cases
        # 数据的存储
    def test_result_transform_and_storage(self,para):
        logger.info("test results storage starting.")
        temp= TestResultBase()
        temp.testTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        for i in range(self.tableWidget_test_results.rowCount()):
           temp.testItems.append({'test_item':self.tableWidget_test_results.item(i,1).text(),\
                                 'test_condition':self.tableWidget_test_results.item(i,2).text(), \
                                 'test_results': self.tableWidget_test_results.item(i, 3).text(), \
                                  'test_conclusion': self.tableWidget_test_results.item(i, 4).text()
                                       })
        print('test_result_storage_obj.testTime:', temp.testTime)
        print('test_result_storage_obj.toJSON():', temp.toJSON())
        ThTestResultsStorage.test_case_result_storage(temp)
        logger.info("test results storage finish.")
    def deal_signal_test_duration_caculate_emit_slot(self, para):
        """
        test case running duration signal process
        :param paras: none
        :return:none
        """
        try:
            hours, remainder = divmod(para, 3600)
            minutes, seconds = divmod(remainder, 60)
            self.label_test_duration.setText(str(int(hours)) + ":" + str(int(minutes)) + ":" + str(int(seconds)))
        except BaseException as e:
            logger.info("ecom ns1 deal_signal_test_duration_caculate_emit_slot fail:" + str(e))
    def start_caculate_test_duration(self):
        if not self.test_time_update_obj:
            self.test_time_update_obj = ThThreadTimerUpdateTestTime()

        self.test_time_update_obj.restart()
        self.test_time_update_obj._signal.connect(self.deal_signal_test_duration_caculate_emit_slot)
        if not self.test_time_update_obj.thread_status:
            self.test_time_update_obj.start()

class test_results:
    def __init__(self):
        self.test_item=''
        self.test_condition=''
        self.test_results=''
        self.test_conclusion=''

if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    vhf=VHFradioMain()
    vhf.show()
    sys.exit(app.exec_())
