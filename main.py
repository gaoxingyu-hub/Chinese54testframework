from MainWindow import MainWindow
from PyQt5 import QtWidgets,QtCore
import sys,getopt
import frozen_dir
from common.info import SystemLanguage
import os
SETUP_DIR = frozen_dir.app_path()

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    try:
        opts, args = getopt.getopt(sys.argv[1:], "ho:", ["help", "lang="])
        for o, a in opts:
            if "lang" in o:
                if a == "en":
                    SystemLanguage.LANGUAGE = SystemLanguage.en_US
                elif a == "zh-CN":
                    SystemLanguage.LANGUAGE = SystemLanguage.ZH_CN
                elif a == "fr":
                    SystemLanguage.LANGUAGE = SystemLanguage.fr_FR
    except getopt.GetoptError:
        sys.exit(2)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec_())
