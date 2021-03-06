# -*- coding: utf-8 -*-


from PyQt5.QtCore import pyqtSlot
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import *
from common.config import TestModuleConfigNew, SystemConfig
from common.th_thread_model import ThThreadTimerUpdateTestTime
from modules.info.testInfo import TestInfo
import os
import frozen_dir
from common.logConfig import Logger
import time

from modules.general.PIC_TEXT import DialogPicText
from .ECOM_NS_1_CONSTANT import ModuleConstants
from .Ui_ECOM_NS1_MAIN import Ui_Dialog
from modules.general.SIMPLE_TEST_PROCESS_1BTN import DialogSimpleTestProcess1Btn
from modules.general.SIMPLE_TEST_PROCESS_2BTN import DialogSimpleTestProcess2Btn
from .ECOM_NS1_KEY_TEST import DialogEcomNs1KeyTest
from common.info import Constants
from database.data_storage import ThTestResultsStorage
from database.test_results_model import TestResultBase
from datetime import datetime

SETUP_DIR = frozen_dir.app_path()
logger = Logger.module_logger("ecom_ns_1")


class EcomNs1Main(QDialog, Ui_Dialog):
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
        super(EcomNs1Main, self).__init__(parent)
        self.setupUi(self)

        self.current_test_step = 0

        self.config_file_path = os.path.join(
            SETUP_DIR, "conf", "ecom_ns_1.json")
        self.system_config_file_path = os.path.join(
            SETUP_DIR, "conf", "system.json")
        self.test_config = TestModuleConfigNew(self.config_file_path)

        self.pic_file_path = os.path.join(
            SETUP_DIR, "imgs", "ecom_ns_1")

        self.system_config = SystemConfig(self.system_config_file_path)
        self.steps2Name = self.system_config.step2name

        self.test_time_update_obj = ThThreadTimerUpdateTestTime()

        self.selected_test_cases = None  # 用来记录选中的测试项目
        self.test_cases_records = None  # 用来记录测试项目的执行测试的进度
        self.current_test_case = None  # 记录当前执行的test case

        self.last_test_case_status = ""
        self.last_test_case_result = ""

        # init tree widget for test case
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
        logger.info("ecom_ns_1 inited")
    
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

    def test_process_control(self, action):
        """
        action: test execute action "next" or "restart" or "finish"
        """
        try:
            if action == "next":
                for case, step in self.test_cases_records.items():
                    if step["current"] > step["max"]:
                        continue
                    # get the test case detail parameters
                    for x in range(len(self.test_config.test_case)):
                        if case in self.test_config.test_case_detail[x]["title"]:

                            temp_test_process = self.test_config.test_case_detail[x]["steps"][step["current"] - 1]
                            self.current_test_case = case

                            self.current_test_step_dialog = globals()[temp_test_process['module']]()
                            self.current_test_step_dialog._signalFinish.connect(self.deal_signal_test_step_finish_emit_slot)

                            self.pic_file_path = os.path.join(
                                SETUP_DIR, "imgs", "ecom_ns", self.test_config.test_case_detail[x]["case_name"])

                            if temp_test_process['module'] == "DialogSimpleTestProcess1Btn":
                                if self.last_test_case_status == ModuleConstants.PROCESS_CONTROL_NEXT:
                                    self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'], "")
                                    self.current_test_step_dialog.set_button_contents(ModuleConstants.BUTTON_CONTENTS_NEXT)
                                    self.current_test_step_dialog.set_msg(Constants.SIGNAL_NEXT)
                                else:
                                    self.current_test_step_dialog\
                                        .set_contents(temp_test_process['title'][:-2] + ModuleConstants.CONTENTS_NOT + temp_test_process['title'][-2:],
                                                       temp_test_process['contents'][:-2] + ModuleConstants.CONTENTS_NOT + temp_test_process['contents'][-2:],
                                                      "")
                                    self.current_test_step_dialog.set_button_contents(ModuleConstants.BUTTON_CONTENTS_FINISH)
                                    self.current_test_step_dialog.set_msg(Constants.SIGNAL_FINISH)
                            elif temp_test_process['module'] == "DialogSimpleTestProcess2Btn":
                                self.current_test_step_dialog.set_button_contents([ModuleConstants.CONTENTS_YES,
                                                                                   ModuleConstants.CONTENTS_NO])
                                self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                           temp_test_process['contents'],
                                                                           os.path.join(
                                                                               self.pic_file_path,
                                                                               temp_test_process['img']))
                            else:
                                self.current_test_step_dialog.set_contents(temp_test_process['title'],
                                                                       temp_test_process['contents'],
                                                                       os.path.join(
                                                                           self.pic_file_path,
                                                                           temp_test_process['img']))
                            self.current_test_step_dialog.exec_()
                            break
            elif action == ModuleConstants.PROCESS_CONTROL_FINISH:
                logger.info(str(self.test_result))
                self.test_result_transform_and_storage()
                self.test_result_display()
        except BaseException as e:
            logger.error(str(e))

        return

    def deal_signal_test_step_finish_emit_slot(self, flag, para):
        """
        child dialog event process handler
        :param flag: string event information
        :param para: object parameters
        :return:none
        """
        if flag == Constants.SIGNAL_TEST_RESULT:
            self.test_result.update(para)
            return

        if self.current_test_step_dialog:
            self.current_test_step_dialog.close()
            self.last_test_case_status = flag
            self.last_test_case_result = para
            if flag == ModuleConstants.PROCESS_CONTROL_FINISH:
                self.test_process_control(ModuleConstants.PROCESS_CONTROL_FINISH)
                logger.info(self.test_result)
                self.test_result_transform_and_storage()
                self.test_result_display()
                return

            if flag != ModuleConstants.PROCESS_CONTROL_NEXT:
                for x in range(len(self.test_config.test_case)):
                    for test_step in self.test_config.test_case_detail[x]["steps"]:
                        if test_step["title"] == flag and test_step["category"] == "execute":
                            self.test_result.update(para)
            self.test_cases_records[self.current_test_case]["current"] = \
                self.test_cases_records[self.current_test_case]["current"] + 1
            # time.sleep(0.1)
            self.test_process_control(ModuleConstants.PROCESS_CONTROL_NEXT)

        temp_flag = False
        for case, step in self.test_cases_records.items():
            if step["current"] <= step["max"]:
                temp_flag = True

        if not temp_flag and self.start_test_flag:
            QMessageBox.information(self, "", ModuleConstants.QMESSAGEBOX_CONTENTS_TEST_FINISH)
            self.start_test_flag = False
            self.test_process_control(ModuleConstants.PROCESS_CONTROL_FINISH)

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

    """
    def treeWidget_item_click_slot_test(self, QTreeWidgetItem, index):
        
        set the test case single checked
        :return: None
        
        for item in self.treeWidget.findItems("", Qt.MatchContains | Qt.MatchRecursive):
            if item.parent() is None:
                continue
            if item.text(0) != QTreeWidgetItem.text(0):
                item.setCheckState(0, Qt.Unchecked)
    """
    def test_result_transform_and_storage(self):
        """
        test result transform and combines to TestResultBase Object
        test result storage
        :return:
        """
        logger.info("test results storage starting.")

        test_result_storage_obj = TestResultBase()
        for key,value in self.test_result.items():
            test_result_storage_obj.testItems.append({key: value})

        test_result_storage_obj.testTime = datetime.now().strftime('%Y-%m-%d %H:%H:%S')
        ThTestResultsStorage.test_case_result_storage(test_result_storage_obj)
        logger.info("test results storage finish.")

    def test_result_display(self):
        """
        display the test result into table widget
        :return: none
        """
        while self.tableWidget_test_results.rowCount() > 0:
            self.tableWidget_test_results.removeRow(0)
        self.tableWidget_test_results.setRowCount(len(self.test_result))
        temp_index = 0
        for key, value in self.test_result.items():
            item = QTableWidgetItem(str(temp_index + 1))
            self.tableWidget_test_results.setItem(temp_index, 0, item)

            item = QTableWidgetItem(str(key))
            self.tableWidget_test_results.setItem(temp_index, 1, item)

            item = QTableWidgetItem(str(value))
            self.tableWidget_test_results.setItem(temp_index, 2, item)

            item = QTableWidgetItem(str(value))
            self.tableWidget_test_results.setItem(temp_index, 3, item)

            item = QTableWidgetItem(str(temp_index + 1))
            for a in range(0, 4):
                self.tableWidget_test_results.item(temp_index, a).setTextAlignment(Qt.AlignCenter)

            temp_index = temp_index + 1
