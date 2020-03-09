# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\code\54testframework\ui\MainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1280, 1024)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        MainWindow.setLayoutDirection(QtCore.Qt.LeftToRight)
        MainWindow.setStyleSheet("QGroupBox{\n"
"font-size:14px;\n"
"font-family:Microsoft YaHei;\n"
"}\n"
"\n"
"QMainWindow::title{\n"
"background-color:#D0DAE5;\n"
"font-color:rgb(255, 255, 255);\n"
"}\n"
"\n"
"")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.groupBoxMenu = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBoxMenu.setStyleSheet("background-color:#D0DAE5;\n"
"color:#666666")
        self.groupBoxMenu.setObjectName("groupBoxMenu")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.groupBoxMenu)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.treeWidget = QtWidgets.QTreeWidget(self.groupBoxMenu)
        self.treeWidget.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.treeWidget.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.treeWidget.setAutoScroll(False)
        self.treeWidget.setIconSize(QtCore.QSize(0, 0))
        self.treeWidget.setHeaderHidden(True)
        self.treeWidget.setObjectName("treeWidget")
        item_0 = QtWidgets.QTreeWidgetItem(self.treeWidget)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        item_1 = QtWidgets.QTreeWidgetItem(item_0)
        self.gridLayout_3.addWidget(self.treeWidget, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBoxMenu)
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Microsoft YaHei")
        font.setPointSize(-1)
        self.groupBox.setFont(font)
        self.groupBox.setStyleSheet("background-color:#D0DAE5;\n"
"color:#666666")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.horizontalLayout.addWidget(self.groupBox)
        self.horizontalLayout.setStretch(0, 3)
        self.horizontalLayout.setStretch(1, 7)
        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(10)
        sizePolicy.setHeightForWidth(self.toolBar.sizePolicy().hasHeightForWidth())
        self.toolBar.setSizePolicy(sizePolicy)
        self.toolBar.setStyleSheet("background-color:#172545;\n"
"height:30px;\n"
"border:None;\n"
"padding:1px;\n"
"font-size:14px;\n"
"font-family:Microsoft YaHei;\n"
"color: #FFFFFF;")
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.TopToolBarArea, self.toolBar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.action_about = QtWidgets.QAction(MainWindow)
        self.action_about.setObjectName("action_about")
        self.action_help = QtWidgets.QAction(MainWindow)
        self.action_help.setObjectName("action_help")
        self.toolBar.addAction(self.action_about)
        self.toolBar.addAction(self.action_help)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "FKJ通信维修分系统"))
        self.groupBoxMenu.setTitle(_translate("MainWindow", "测试模块"))
        self.treeWidget.headerItem().setText(0, _translate("MainWindow", "1"))
        __sortingEnabled = self.treeWidget.isSortingEnabled()
        self.treeWidget.setSortingEnabled(False)
        self.treeWidget.topLevelItem(0).setText(0, _translate("MainWindow", "通信分系统"))
        self.treeWidget.topLevelItem(0).child(0).setText(0, _translate("MainWindow", "散射高频设备"))
        self.treeWidget.topLevelItem(0).child(1).setText(0, _translate("MainWindow", "MW-1500微波电台"))
        self.treeWidget.topLevelItem(0).child(2).setText(0, _translate("MainWindow", "ECOM_NS_1型交换机"))
        self.treeWidget.topLevelItem(0).child(3).setText(0, _translate("MainWindow", "ECOM_NS_2型交换机"))
        self.treeWidget.topLevelItem(0).child(4).setText(0, _translate("MainWindow", "VHF电台"))
        self.treeWidget.topLevelItem(0).child(5).setText(0, _translate("MainWindow", "自组网微波通信设备"))
        self.treeWidget.topLevelItem(0).child(6).setText(0, _translate("MainWindow", "SDSL设备"))
        self.treeWidget.topLevelItem(0).child(7).setText(0, _translate("MainWindow", "IP保密机"))
        self.treeWidget.topLevelItem(0).child(8).setText(0, _translate("MainWindow", "通信控制设备"))
        self.treeWidget.topLevelItem(0).child(9).setText(0, _translate("MainWindow", "路由器"))
        self.treeWidget.setSortingEnabled(__sortingEnabled)
        self.groupBox.setTitle(_translate("MainWindow", "测试项目"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.action_about.setText(_translate("MainWindow", "关于"))
        self.action_about.setToolTip(_translate("MainWindow", "<html><head/><body><p><img src=\":/newPrefix/icon/start1.ico\"/></p></body></html>"))
        self.action_help.setText(_translate("MainWindow", "帮助"))
        self.action_help.setToolTip(_translate("MainWindow", "<html><head/><body><p><img src=\":/newPrefix/icon/start1.ico\"/></p></body></html>"))
import res.iconQrc_rc


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
