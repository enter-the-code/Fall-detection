import time
import os
import sys
import serial
import math
import datetime

# PySide imports
from PySide2 import QtGui
from PySide2.QtCore import QTimer, Qt, QThread, Signal
from PySide2.QtGui import QKeySequence
from PySide2.QtWidgets import (
    QAction,
    QTabWidget,
    QGridLayout,
    QGroupBox,
    QLineEdit,
    QLabel,
    QPushButton,
    QComboBox,
    QFileDialog,
    QMainWindow,
    QWidget,
    QCheckBox,
    QApplication,
    QShortcut,
    QStatusBar,
    QMessageBox
)

# ini config imports
from configparser import ConfigParser, NoOptionError


# MACRO constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONNECT_N_MSG = "Not Connected"
CONNECT_Y_MSG = "Connected"
DEMO_LIST = ["People Count", "Out of Box"]


class Window(QMainWindow):
    def __init__(self, parent=None, size=[], title="app"):
        super().__init__(parent)

        self.core = Core()

        # part widget declare
        self.initConnectBox()
        self.initCfgBox()

        # icon
        self.setWindowIcon(QtGui.QIcon(BASE_DIR + "/img/bm_icon.png"))

        # Layout setting
        self.gridLayout = QGridLayout()
        self.central = QWidget()
        self.central.setLayout(self.gridLayout)
        self.gridLayout.addWidget(self.connectBox, 0, 0)
        self.gridLayout.addWidget(self.cfgBox, 1, 0)

        self.setStatusBar(QStatusBar(self)) # bottom bar that explains tooltips
        self.statusBar().showMessage("Status Description")


        # TODO : min size setting - dynamic?
        # self.setMinimumHeight(450)
        self.setMinimumWidth(350)

        # Shortcut
        self.shortcut = QShortcut(QKeySequence("Ctrl+W"), self) # ctrl+W to close program
        self.shortcut.activated.connect(self.close)

        self.setCentralWidget(self.central)
        self.setWindowTitle(title)

    def initConnectBox(self):
        # outter box
        self.connectBox = QGroupBox("Connection")
        self.connectLayout = QGridLayout()
        self.connectBox.setLayout(self.connectLayout)
        self.connectCfgLayout = QGridLayout()
        self.connectBtnLayout = QGridLayout()
        self.connectLayout.addLayout(self.connectCfgLayout, 0, 0)
        self.connectLayout.addLayout(self.connectBtnLayout, 1, 0)

        # inner component
        self.connectCfgLayout.addWidget(QLabel("Demo"), 0, 0)
        self.demoList = QComboBox()
        self.demoList.addItems(DEMO_LIST)
        self.connectCfgLayout.addWidget(self.demoList, 0, 1)
        self.demoList.setCurrentIndex(0)

        self.connectCfgLayout.addWidget(QLabel("CLI COM"), 1, 0)
        self.cli_num_line = QLineEdit("")
        self.cli_num_line.setToolTip("Enhanced Port")
        self.connectCfgLayout.addWidget(self.cli_num_line, 1, 1)
        
        self.connectCfgLayout.addWidget(QLabel("Data COM"), 2, 0)
        self.data_num_line = QLineEdit("")
        self.data_num_line.setToolTip("Standard Port")
        self.connectCfgLayout.addWidget(self.data_num_line, 2, 1)

        self.connectStatus = QLabel(CONNECT_N_MSG)
        self.connectStatus.setAlignment(Qt.AlignCenter)
        self.connectBtnLayout.addWidget(self.connectStatus, 0, 0)
        self.connectBtn = QPushButton("Connect")
        self.connectBtn.setMaximumWidth(100)
        self.connectBtnLayout.addWidget(self.connectBtn, 0, 1)

        # signal connection
        self.demoList.currentIndexChanged.connect(self.demoChanged)
        self.connectBtn.clicked.connect(self.startConnect)

    def initCfgBox(self):
        # outter box
        self.cfgBox = QGroupBox("Config")
        self.cfgLayout = QGridLayout()
        self.cfgBox.setLayout(self.cfgLayout)

        # inner box
        self.filenameCfg = QLineEdit()
        self.cfgLayout.addWidget(self.filenameCfg, 0, 0)

        self.selectCfgBtn = QPushButton("Select config")
        self.selectCfgBtn.setFixedWidth(100)
        self.cfgLayout.addWidget(self.selectCfgBtn, 0, 1)

        self.sendCfgBtn = QPushButton("Start with config")
        self.sendCfgBtn.setEnabled(False)
        self.cfgLayout.addWidget(self.sendCfgBtn, 1, 0, 1, 2)

        # signal connection
        self.selectCfgBtn.clicked.connect(lambda: self.selectCfg(self.filenameCfg))
        self.sendCfgBtn.clicked.connect(self.startSensor)

    
    def startConnect(self):
        if(self.connectStatus.text() == CONNECT_N_MSG):
            self.statusBar().showMessage("Start connect")
            # REF : onConnect(self)
            

    def demoChanged(self):
        self.statusBar().showMessage("Demo : " + self.demoList.currentText())
        # REF : onChangeDemo

    def selectCfg(self, cfgLine):
        self.statusBar().showMessage("Select configuartion file")
        # REF : core.selectCfg

        try:
            fname = self.core.selectFile(cfgLine)
            # TODO : record it on ini
            self.core.parseCfg(fname)
        except:
            self.cfg_failed_warn = QMessageBox.warning(
                self, "Parse error", "cfg Parsing failed"
            )

    def startSensor(self):
        self.statusBar().showMessage("Send config and start")
        # REF : core.sendCfg

class Core:
    def __init__(self):
        self.parser = UARTParser()
        self.demo = DEMO_LIST[0]

    def selectFile(self, fLine: QLineEdit):
        try:
            cfg_dir = BASE_DIR
            path = ""   # TODO : recover from ini
            if path != "":
                cfg_dir = path
        except:
            cfg_dir = ""

        fname = QFileDialog.getOpenFileName(caption="Open .cfg File", dir=cfg_dir, filter="cfg(*.cfg)")
        fLine.setText(str(fname[0]))
        return fname[0]

    def parseCfg(self, fname):
        with open(fname, "r") as cfg_file:
            self.cfg_lines = cfg_file.readlines()
            self.parser.cfg = self.cfg_lines
            self.parser.demo = self.demo
        # TODO : cotinue from 498




class UARTParser():
    def __init__(self):
        pass
    # self.parserType는 DoubleCOMPort로 고정


class parseUartThread(QThread):
    fin = Signal(dict)

    def __init__(self): # uParser 받지 않음
            QThread.__init__(self)

    def run(self):
        outputDict = self.parser.readAndParseUartSingleCOMPort()
        self.fin.emit(outputDict)

    def stop(self):
        self.terminate()


if __name__ == '__main__':
    # may not use app screen size
    app = QApplication(sys.argv)
    screen = app.primaryScreen()
    size = screen.size()
    main = Window(size=size, title="Batch Maker : Fall Detect")
    main.show()
    sys.exit(app.exec_())