from PyQt5.QtCore import pyqtSlot, QPoint, Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QDialog, QGraphicsItem
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtGui, QtWidgets, QtCore
import os
from modules.VHF_radio.Ui_TEST2 import Ui_Dialog
from PyQt5.QtCore import pyqtSignal
from common.info import Constants
from PyQt5 import QtGui
from common.logConfig import Logger
from PyQt5.QtWidgets import QMessageBox
from modules.VHF_radio.VHF_radio_CONSTANT import ModuleConstants

logger = Logger.module_logger("DialogTest7point5")


class DialogTest7point5(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    signalTest = pyqtSignal(object)
    signalPrint = pyqtSignal(object)
    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(DialogTest7point5, self).__init__(parent)
        self.setupUi(self)
        self.state=''
        self.test_result = test_results()
        self.action = 'finish_all'
    @pyqtSlot()
    def on_pushButton_1_clicked(self):

        if self.state=='7.5':
            self.test_result.test_item = "测试面板收发指示灯的变化"
            self.test_result.test_condition = ''
            self.test_result.test_results = '音频模块故障'
            self.test_result.test_conclusion = 'PASS'
            QMessageBox.information(self, "提示", "音频模块故障", QMessageBox.Ok)
        if self.state=='26':
            self.test_result.test_item = "测试被测电台"
            self.test_result.test_condition = ''
            self.test_result.test_results = '综合业务模块故障'
            self.test_result.test_conclusion = 'FAIL'
            QMessageBox.information(self, "提示", "综合业务模块故障", QMessageBox.Ok)
        self.signalTest.emit('test')
        self.signalPrint.emit('print')
        self.close()


    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        if self.state == '7.5':
            self.test_result.test_item = "测试面板收发指示灯的变化"
            self.test_result.test_condition = ''
            self.test_result.test_results = '中频模块故障'
            self.test_result.test_conclusion = 'FAIL'
            QMessageBox.information(self, "提示", "中频模块故障", QMessageBox.Ok)
        if self.state == '26':
            self.test_result.test_item = "被测电台通话时的侧音"
            self.test_result.test_condition = ''
            self.test_result.test_results = '音频模块故障'
            self.test_result.test_conclusion = 'FAIL'
            QMessageBox.information(self, "提示", "音频模块故障", QMessageBox.Ok)
        self.signalTest.emit('test')
        self.signalPrint.emit('print')
        self.close()
    def set_contents(self, title, contents,img_file_path ):
        try:
            self.setWindowTitle(title)
            self.textBrowser_contents.setText(contents)
            if img_file_path and img_file_path != "":
                if os.path.isfile(img_file_path) and os.access(img_file_path, os.W_OK):
                    self.pixmap = QtGui.QPixmap(img_file_path)
                    self.pixmap = self.pixmap.scaled(600, 600,
                                                     Qt.IgnoreAspectRatio | Qt.SmoothTransformation)
                    self.label_img.setPixmap(self.pixmap)
                    self.label_img.setAlignment(Qt.AlignCenter)
        except BaseException as e:
            logger.error(str(e))
        return

    def set_state(self, state):
        self.state = state

    @pyqtSlot()
    def closeEvent(self, event):
        if self.action == 'finish_all':
            self.signalFinish1.emit('finish_all', None)
        event.accept()
class test_results:
    def __init__(self):
        self.test_item=''
        self.test_condition=''
        self.test_results=''
        self.test_conclusion=''