import time
import os
import sys
import serial
import math
import datetime

# PySide imports
from PySide2 import QtGui
from PySide2.QtCore import QTimer, Qt, QThread, Signal
from PySide2.QtGui import QKeySequence, QIntValidator
from PySide2.QtWidgets import (
    QAction,
    QGridLayout,
    QGroupBox,
    QLineEdit,
    QLabel,
    QPushButton,
    QComboBox,
    QFileDialog,
    QMainWindow,
    QWidget,
    QApplication,
    QShortcut,
    QStatusBar,
    QMessageBox
)

# ini config imports
from configparser import ConfigParser, NoOptionError


# MACRO constants
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INI_FILE_NAME = "batch_maker.ini"
INI_PATH = os.path.join(BASE_DIR, INI_FILE_NAME)
CONNECT_N_MSG = "Not Connected"
CONNECT_Y_MSG = "Connected"
DEMO_LIST = ["People Count", "Out of Box"]


class Window(QMainWindow):
    def __init__(self, parent=None, title="app"):
        super().__init__(parent)

        self.core = Core(self)

        # ini parser setting
        self.iniParser = ConfigParser()
        if not os.path.exists(INI_PATH):
            self.core.ini_create(self.iniParser)
        
        self.iniParser.read(INI_PATH)
        if self.iniParser.sections() == []: # file with no contents
            self.core.ini_create(self.iniParser)

        self.demo_idx = self.core.ini_get_demo(self.iniParser)
        self.cli_com = self.core.ini_get_cli_com(self.iniParser)
        self.data_com = self.core.ini_get_data_com(self.iniParser)
        self.cfg_path = self.core.ini_get_cfg_path(self.iniParser)

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
        self.demoList.setCurrentIndex(self.demo_idx)

        self.connectCfgLayout.addWidget(QLabel("CLI COM"), 1, 0)
        self.cli_num_line = QLineEdit(self.cli_com)
        self.cli_num_line.setToolTip("Enhanced Port")
        self.connectCfgLayout.addWidget(self.cli_num_line, 1, 1)
        
        self.connectCfgLayout.addWidget(QLabel("Data COM"), 2, 0)
        self.data_num_line = QLineEdit(self.data_com)
        self.data_num_line.setToolTip("Standard Port")
        self.connectCfgLayout.addWidget(self.data_num_line, 2, 1)

        self.connectStatus = QLabel(CONNECT_N_MSG)
        self.connectStatus.setAlignment(Qt.AlignCenter)
        self.connectBtnLayout.addWidget(self.connectStatus, 0, 0)
        self.connectBtn = QPushButton("Connect")
        self.connectBtn.setMaximumWidth(100)
        self.connectBtnLayout.addWidget(self.connectBtn, 0, 1)

        # COM Port range restriction
        self.COM_valid = QIntValidator(1, 256)
        self.cli_num_line.setValidator(self.COM_valid)
        self.data_num_line.setValidator(self.COM_valid)

        # signal connection
        self.demoList.currentIndexChanged.connect(self.demoChanged)
        self.connectBtn.clicked.connect(self.startConnect)

    def initCfgBox(self):
        # outter box
        self.cfgBox = QGroupBox("Config")
        self.cfgLayout = QGridLayout()
        self.cfgBox.setLayout(self.cfgLayout)

        # inner box
        self.filenameCfg = QLineEdit(self.cfg_path)
        self.filenameCfg.setReadOnly(True)
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
        self.demo_idx = self.demoList.currentIndex()
        self.statusBar().showMessage("Demo : " + self.demoList.currentText())
        # REF : onChangeDemo

    def selectCfg(self, cfgLine):
        self.statusBar().showMessage("Select configuartion file")
        # REF : core.selectCfg

        fname = self.core.selectFile(cfgLine)
        try:
            self.core.parseCfg(fname)
        except Exception as e:
            self.cfg_failed_warn = QMessageBox.warning(
                self, "Cfg selection error", repr(e)
            )

    def startSensor(self):
        self.statusBar().showMessage("Send config and start")
        # REF : core.sendCfg

    def closeEvent(self, event):
        event.accept()
        self.core.ini_save(self.iniParser)
        QApplication.quit()

class Core:
    def __init__(self, window: Window):
        self.parser = UARTParser()
        self.demo = DEMO_LIST[0]
        self.window = window

    def selectFile(self, fLine: QLineEdit):
        try:
            cfg_dir = BASE_DIR
            # recover dir from ini
            path = fLine.text()
            if path != "":
                cfg_dir = os.path.dirname(path)
                if not os.path.exists(cfg_dir):
                    cfg_dir = ""
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

    
    # INI Parse
    def ini_get_demo(self, parser: ConfigParser):
        self.demo_idx = self.window.iniParser.getint(
            "Selection", "demo_idx", fallback=0
        )
        if self.demo_idx >= len(DEMO_LIST):
            self.demo_idx = 0
        return self.demo_idx
    
    def ini_get_cli_com(self, parser: ConfigParser):
        self.cli_com = self.window.iniParser.get(
            "Selection", "cli_com", fallback=""
        )
        try:
            if (self.cli_com != "") and ((int(self.cli_com) < 1) or (int(self.cli_com) > 256)):
                self.cli_com = ""
        except ValueError:
                self.cli_com = ""
        return self.cli_com
    
    def ini_get_data_com(self, parser: ConfigParser):
        self.data_com = self.window.iniParser.get(
            "Selection", "data_com", fallback=""
        )
        try:
            if (self.data_com != "") and ((int(self.data_com) < 1) or (int(self.data_com) > 256)):
                self.data_com = ""
        except ValueError:
                self.data_com = ""
        return self.data_com

    def ini_get_cfg_path(self, parser: ConfigParser):
        self.cfg_path = self.window.iniParser.get(
            "Selection", "cfg_path", fallback=""
        )
        if not os.path.exists(self.cfg_path):
            self.cfg_path = ""
        return self.cfg_path

    def ini_create(self, parser: ConfigParser):
        if "Selection" not in parser:
            parser["Selection"] = {
                "Demo_idx" : "0",
                "CLI_COM" : "",
                "Data_COM" : "",
                "cfg_path" : ""
            }

        self.ini_write(parser)

    def ini_write(self, parser: ConfigParser):
        with open(INI_PATH, "w", encoding="UTF-8") as ini_file:
            parser.write(ini_file)
    
    def ini_save(self, parser: ConfigParser):
        parser["Selection"]["Demo_idx"] = str(self.window.demo_idx)
        parser["Selection"]["cli_com"] = self.window.cli_num_line.text()
        parser["Selection"]["data_com"] = self.window.data_num_line.text()
        parser["Selection"]["cfg_path"] = self.window.filenameCfg.text()
        
        self.ini_write(parser)


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
    # # may not use app screen size
    app = QApplication(sys.argv)
    main = Window(title="Batch Maker : Fall Detect")
    main.show()
    sys.exit(app.exec_())