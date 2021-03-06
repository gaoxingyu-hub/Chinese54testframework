# -*- coding: utf-8 -*-

"""
Module implementing PIC_TEXT.
"""

from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QDialog
from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal

from .Ui_AUTO_TEST_FILTER import Ui_Dialog
import os
from InstrumentDrivers.VNADriver import AgilentN5242
from PyQt5.Qt import QMessageBox
import numpy as np
from .high_freq_constant import ModuleConstants

class AUTO_TEST_FILTER(QDialog, Ui_Dialog):
    """
    Class documentation goes here.
    """
    _signalTest = pyqtSignal(str)
    _signalFinish = pyqtSignal(str,object)

    def __init__(self, parent=None):
        """
        Constructor
        
        @param parent reference to the parent widget
        @type QWidget
        """
        super(AUTO_TEST_FILTER, self).__init__(parent)
        self.setupUi(self)
        self.flag = 1
        self.demo = True
        self.action = 'finish_all'
    
    def initUi(self,mConfig):
        self.addr_na= ModuleConstants.IP_NA
        freq_na= mConfig.test_case_detail[4]["test_para"][0]
        bw_na= mConfig.test_case_detail[4]["test_para"][1]

        self.lineEdit_freq_na.setText(freq_na)
        self.lineEdit_bw_na.setText(bw_na)
        self.thresholdL_1 = float(mConfig.test_case_detail[4]["threshold"][0])
        self.thresholdH_1 = float(mConfig.test_case_detail[4]["threshold"][1])
        self.thresholdL_2 = float(mConfig.test_case_detail[4]["threshold"][2])
        self.thresholdH_2 = float(mConfig.test_case_detail[4]["threshold"][3])

    def set_contents(self,title,contents):
        self.setWindowTitle(title)
#         self.textBrowser_contents.setText(contents)
        # if os.access(img_file_path, os.W_OK):
        #     self.label_img.setPixmap(QtGui.QPixmap(img_file_path))
        # return
    
    @pyqtSlot()
    def on_pushButton_next_clicked(self):
        """
        Slot documentation goes here.
        """
        # TODO: not implemented yet
        try:
            self.freq_na=float(self.lineEdit_freq_na.text())*1e6
            self.bw_na=float(self.lineEdit_bw_na.text())*1e6
            addr_na=str(self.addr_na)
        except:
            QMessageBox.warning(self, ModuleConstants.QMESSAGEBOX_WARN, 
                                ModuleConstants.QMESSAGEBOX_WARN_INPUT_PARAMETER_NOT_ENOUGH)
            return
        addr_na="TCPIP0::"+addr_na+"::inst0::INSTR"

        self.test_result=test_results()
        if not self.demo:
            try:
                self.na=AgilentN5242.VNA_AgilentN5242(addr_na)
            except:
                QMessageBox.warning(self,ModuleConstants.QMESSAGEBOX_WARN, 
                                    ModuleConstants.QMESSAGEBOX_WARN_INSTR_NOT_VALID)
                return
        self.test_result.test_item = ModuleConstants.TESTITEM_FILTER
        self.test_result.test_condition = ModuleConstants.TESTCONDITION_FREQ+self.lineEdit_freq_na.text()+\
                                          ModuleConstants.TESTCONDITION_FREQ_UNIT+'，'+ModuleConstants.TESTCONDITION_BAND+\
                                          self.lineEdit_bw_na.text()+ModuleConstants.TESTCONDITION_BAND_UNIT
        mTemp=self.testProcess()
        self.test_result.test_results='S11: '+str(mTemp[0])+' S21: '+str(mTemp[1])
        if self.thresholdL_1<mTemp[0]<self.thresholdH_1 and self.thresholdL_2<mTemp[1]<self.thresholdH_2:
            QMessageBox.information(self,ModuleConstants.QMESSAGEBOX_INFO,ModuleConstants.QMESSAGEBOX_CONTENTS_TEST_NORMAL,QMessageBox.Ok)
            self.test_result.test_conclusion=ModuleConstants.TESTRESULT_PASS
        else:
            QMessageBox.information(self,ModuleConstants.QMESSAGEBOX_INFO,ModuleConstants.TESTITEM_FILTER+
                                    ModuleConstants.QMESSAGEBOX_CONTENTS_TEST_ABNORMAL,QMessageBox.Ok)
            self.test_result.test_conclusion=ModuleConstants.TESTRESULT_FAIL
        self._signalTest.emit("test")
        self.accept()
        self.close()
    
    
    def testProcess(self):
        temp =[]
        if not self.demo:
            self.na.SetCentreFreq(self.freq_na)
            self.na.SetSpan(self.bw_na)
            self.na.SelectMeas('1')
            self.na.SetMarkerMode('NORM')
            self.na.SetMarkerX(self.freq_na)
            mTemp1 = float(self.na.GetMarkerY())
            mTemp1 = round(mTemp1,3)
            self.na.SelectMeas('2')
            self.na.SetMarkerX(self.freq_na)
            mTemp2 = float(self.na.GetMarkerY())
            mTemp2 = round(mTemp2,3)
            temp.append(mTemp1) 
            temp.append(mTemp2)
            
        else:
            temp.append(float(7+ np.random.random(1)))
            temp.append(float(7+ np.random.random(1)))
          
        return temp
    
    @pyqtSlot()
    def closeEvent(self, event):
        if self.action == 'finish_all':
            self._signalFinish.emit('finish_all', None)
        event.accept()
class test_results:
    def __init__(self):
        self.test_item=''
        self.test_condition=''
        self.test_results=0.0
        self.test_conclusion='PASS'
# 
# mres =float(7+ np.random.random(1))
# print(round(mres,3))