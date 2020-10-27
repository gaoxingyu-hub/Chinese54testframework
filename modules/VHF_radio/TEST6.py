from PyQt5.QtCore import pyqtSlot, QPoint, Qt
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtWidgets import QDialog, QGraphicsItem, QScrollArea
from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import pyqtSignal

from modules.VHF_radio.Ui_TEST6 import Ui_Dialog
import os


class DialogTest6(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    test_condition='test_condition'
    signalFinish1 = pyqtSignal(str, object)
    def __init__(self, parent=None):
        """
        Constructor
        @param parent reference to the parent widget
        @type QWidget
        """
        super(DialogTest6, self).__init__(parent)
        self.setupUi(self)
        self.state = ''
        self.demo=True
        self.action = 'finish_all'
    def initUi(self, mConfig):
        if self.state=='6':
            self.lineEdit_1.setText(mConfig.test_case_detail[0]["test_para"][0])
            self.lineEdit_3.setText(mConfig.test_case_detail[0]["test_para"][1])
            self.lineEdit_4.setText(mConfig.test_case_detail[0]["test_para"][2])
            self.lineEdit_5.setText(mConfig.test_case_detail[0]["test_para"][3])
        elif self.state == '7.3':
            self.lineEdit_1.setText(mConfig.test_case_detail[0]["test_para"][0])
            self.lineEdit_3.setText(mConfig.test_case_detail[0]["test_para"][1])
            self.lineEdit_4.setText(mConfig.test_case_detail[0]["test_para"][2])
            self.lineEdit_5.setText(mConfig.test_case_detail[0]["test_para"][4])
    def set_contents(self, title, contents, img_file_path):

        try:
            self.setWindowTitle(title)
            self.textBrowser_contents.setText(contents)
            if img_file_path and img_file_path != "":
                if os.path.isfile(img_file_path) and os.access(img_file_path, os.W_OK):
                    self.pixmap = QtGui.QPixmap(img_file_path)
                    self.pixmap = self.pixmap.scaled(560, 400,
                                                     Qt.KeepAspectRatio | Qt.SmoothTransformation)
                    self.label_img.setPixmap(self.pixmap)
                    self.label_img.setAlignment(Qt.AlignCenter)
        except:
            pass
        return

    @pyqtSlot()
    def on_pushButton_next_clicked(self):
        """
        Slot documentation goes here.
        """
        # 连接矢量信号发生器，上传参数
        if not self.demo:
            pass


        #没有连接矢量信号发生器，没有上传参数
        if self.demo:
           DialogTest6.test_condition=str(self.label_1.text()) +':'+ str(self.lineEdit_1.text()) + str(
              self.comboBox_1.currentText()) +','+ \
                                          str(self.label_2.text()) +':'+str(self.comboBox_2.currentText())+',' + str(
              self.label_3.text()) +':'+ str(self.lineEdit_3.text()) + \
                                          str(self.comboBox_3.currentText())+',' + str(self.label_4.text())+':' + \
                                          str(self.lineEdit_4.text()) + str(self.comboBox_4.currentText()) +','+ str(
              self.label_5.text())+':' + str(self.lineEdit_5.text()) + str(self.comboBox_5.currentText())

        self.signalFinish1.emit("next", None)
        self.close()

    def set_state(self, state):
        self.state = state
    @pyqtSlot()
    def closeEvent(self, event):
        if self.action == 'finish_all':
            self.signalFinish1.emit('finish_all', None)
        event.accept()