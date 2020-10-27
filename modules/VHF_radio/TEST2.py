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

logger = Logger.module_logger("DialogTest2")


class DialogTest2(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    signalTest = pyqtSignal(object)
    signalPrint=pyqtSignal(object)
    signalFinish1 = pyqtSignal(str, object)


    def __init__(self, parent=None):
        """
        Constructor

        @param parent reference to the parent widget
        @type QWidget
        """
        super(DialogTest2, self).__init__(parent)
        self.setupUi(self)
        self.state=''
        self.test_result = test_results()
        self.action = 'finish_all'
    @pyqtSlot()
    def on_pushButton_1_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        self.signalFinish1.emit("next", None)
        self.close()
    @pyqtSlot()
    def on_pushButton_2_clicked(self):
        if self.state=='2':
            self.test_result.test_item="测试VHF电台电源"
            self.test_result.test_condition=''
            self.test_result.test_results='VHF电台电源故障'
            self.test_result.test_conclusion='FAIL'
            QMessageBox.information(self, "提示","VHF电台电源故障", QMessageBox.Ok)
        elif self.state == '3':
            self.test_result.test_item = "测试系统加载"
            self.test_result.test_condition = ''
            self.test_result.test_results = '综合业务模件故障'
            self.test_result.test_conclusion = 'FAIL'
            QMessageBox.information(self, "提示", "综合业务模件故障", QMessageBox.Ok)
        elif self.state=='4':
            self.test_result.test_item = "测试面板操作"
            self.test_result.test_condition = ''
            self.test_result.test_results = '综合业务模件故障'
            self.test_result.test_conclusion = 'FAIL'
            QMessageBox.information(self, "提示", "综合业务模件故障", QMessageBox.Ok)
        elif self.state=='27':
            self.test_result.test_item = "两部电台的语音通话"
            self.test_result.test_condition = ''
            self.test_result.test_results = '综合业务模件故障'
            self.test_result.test_conclusion = 'FAIL'
            QMessageBox.information(self, "提示", "综合业务模块故障", QMessageBox.Ok)

        self.signalTest.emit("test")
        self.signalPrint.emit('print')
        self.close()


    def set_contents(self, title, contents,img_file_path ):
        """
        set gui display information
        :param title: dialog window title
        :param contents: tips
        :param img_file_path:image file full path
        :return: none
        """
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

    def set_state(self,state):
        self.state=state

    @pyqtSlot()
    def closeEvent(self, event):
        if self.action == 'finish_all':
            self.signalFinish1.emit('finish_all', None)
        event.accept()
#
class test_results:
    def __init__(self):
        self.test_item=''
        self.test_condition=''
        self.test_results=''
        self.test_conclusion=''
