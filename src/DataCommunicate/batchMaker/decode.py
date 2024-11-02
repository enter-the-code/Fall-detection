import time
import os
import sys
import serial
import math
import datetime
import numpy as np
import struct

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
CONNECT_NA_MSG = "Unable to Connect"
CONNECT_BTN_MSG = "Connect"
CONNECT_BTN_RESET_MSG = "Reset Connection"
SEND_CFG_BTN_START_MSG = "Start with config"
SEND_CFG_BTN_RUN_MSG = "Sensor now Running"
DEMO_LIST = ["People Count", "Out of Box"]
STATUS_MSG_DELAY = 2000


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

        # status bar setting
        self.setStatusBar(QStatusBar(self)) # bottom bar that explains tooltips
        self.statusBar().addWidget(QLabel("Status Description"))


        # TODO : fixed size set
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
        self.connectBtn = QPushButton(CONNECT_BTN_MSG)
        self.connectBtn.setToolTip("You MUST set COM port before connection")
        self.connectBtn.setMaximumWidth(120)
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

        self.sendCfgBtn = QPushButton(SEND_CFG_BTN_START_MSG)
        self.sendCfgBtn.setEnabled(False)
        self.cfgLayout.addWidget(self.sendCfgBtn, 1, 0, 1, 2)

        # signal connection
        self.selectCfgBtn.clicked.connect(lambda: self.selectCfg(self.filenameCfg))
        self.sendCfgBtn.clicked.connect(self.startSensor)

    
    # REF : onConnect(self) - DONE
    def startConnect(self):
        if(self.connectStatus.text() == CONNECT_N_MSG or self.connectStatus.text() == CONNECT_NA_MSG):
            if self.core.connectCom(self.connectStatus) == 0:
                self.connectBtn.setText(CONNECT_BTN_RESET_MSG)
                self.sendCfgBtn.setEnabled(True)
                self.statusBar().showMessage("Connected", STATUS_MSG_DELAY)
            else:
                self.sendCfgBtn.setEnabled(False)
                self.statusBar().showMessage("Connect Failed", STATUS_MSG_DELAY)
        else:
            self.core.gracefulReset()
            self.connectStatus.setText(CONNECT_N_MSG)
            self.connectBtn.setText(CONNECT_BTN_MSG)
            self.sendCfgBtn.setEnabled(False)   # double check
            self.sendCfgBtn.setText(CONNECT_BTN_MSG)

    # REF : onChangeDemo -> core.changeDemo
    def demoChanged(self):
        self.demo_idx = self.demoList.currentIndex()
        self.statusBar().showMessage("Demo : " + self.demoList.currentText(), STATUS_MSG_DELAY)

    # REF : core.selectCfg
    def selectCfg(self, cfgLine):
        self.statusBar().showMessage("Select configuartion file", STATUS_MSG_DELAY)

        fname = self.core.selectFile(cfgLine)
        if fname == "":
            return  # selection canceled
        try:
            self.core.parseCfg(fname)
            # if parse succed, set text
            cfgLine.setText(fname)
            self.statusBar().showMessage("cfg set : " + os.path.basename(fname), STATUS_MSG_DELAY)
        except Exception as e:
            self.cfg_selec_warn(e)

    def cfg_selec_warn(self, e: Exception):
        self.cfg_failed_warn = QMessageBox.warning(
            self, "Cfg selection error", repr(e)
        )

    def startSensor(self):
        self.statusBar().showMessage("Send config and start")
        if(self.core.sendCfg()):
            # disable button before reset
            self.sendCfgBtn.setDisabled(True)
            self.sendCfgBtn.setText(SEND_CFG_BTN_RUN_MSG)

    def closeEvent(self, event):
        event.accept()
        self.core.ini_save(self.iniParser)
        QApplication.quit()

class Core:
    def __init__(self, window: Window):
        self.parser = UARTParser()
        self.demo = DEMO_LIST[0]
        self.window = window
        self.frameTime = 50

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
        return fname[0]

    def parseCfg(self, fname):
        with open(fname, "r") as cfg_file:
            self.cfg_lines = cfg_file.readlines()
            self.parser.cfg = self.cfg_lines
            self.parser.demo = self.demo

        # TODO verify it really needed
        # code from next func only useful for plot : from line 498

    # Start with config button call this method
    # REF : core.sendCfg
    def sendCfg(self):
        try:
            self.cfg_lines
        except AttributeError:
            try:
                self.parseCfg(self.window.filenameCfg.text())
            except Exception as e:
                self.window.cfg_selec_warn(e)
                return False

        self.parser.uartSendCfg(self.cfg_lines)
        sys.stdout.flush()
        self.parseTimer.start(self.frameTime)
        # it will start self.parseData thread

        return True

    # Connection Handling
    # REF : connectCom()
    def connectCom(self, statusLine: QLabel):
        self.cli_com = int(self.window.cli_num_line.text())
        self.data_com = int(self.window.data_num_line.text())

        # init thread
        self.uart_thread = parseUartThread(self.parser)

        # Notice : timer starts from sendCfg() - binds with sendCfgBtn
        self.parseTimer = QTimer()
        self.parseTimer.setSingleShot(False)
        self.parseTimer.timeout.connect(self.parseData)

        try:
            if os.name == "nt":
                uart = "COM" + str(self.cli_com)
                data = "COM" + str(self.data_com)
            else:
                uart = self.cli_com
                data = self.data_com
            self.parser.connectComPort(uart, data)
            self.window.connectStatus.setText(CONNECT_Y_MSG)
        except:
            self.window.connectStatus.setText(CONNECT_NA_MSG)
            return -1

        return 0

    # REF : gracefulReset()
    def gracefulReset(self):
        self.parseTimer.stop()
        self.uart_thread.stop()
        if self.parser.cliCom is not None:
            self.parser.cliCom.close()
        if self.parser.dataCom is not None:
            self.parser.dataCom.close()

    def parseData(self):
        self.uart_thread.start(priority=QThread.HighestPriority)

    
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
        self.binData = bytearray(0)
        self.uartCounter = 0
    # self.parserType는 DoubleCOMPort로 고정

    def readAndParseUartCOMPort(self):
        self.fail = 0
        index = 0
        # TODO : gui_parser.py line 71
    
    def parseStandardFrame(self, frameData):
        headerStruct = 'Q8I'    # UART binary format what ti sensor often uses
        frameHeaderLen = struct.calcsize(headerStruct)
        tlvHeaderLength = 8

        outputDict = {}
        outputDict['error'] = 0

        totalLenCheck = 0

        # Read the frame Header
        try:
            magic, version, totalPacketLen, platform, frameNum, timeCPUCycles, numDetectedObj, numTLVs, subFrameNum = struct.unpack(headerStruct, frameData[:frameHeaderLen])
        except:
            # header read failed
            outputDict['error'] = 1

        # Move frameData ptr to start of 1st TLV   
        frameData = frameData[frameHeaderLen:]
        totalLenCheck += frameHeaderLen

        # TODO : parseFrame.py line 89

    def connectComPort(self, cliCom, dataCom):
        self.cliCom = serial.Serial(cliCom, 115200, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.6)
        self.dataCom = serial.Serial(dataCom, 921600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, timeout=0.6)
        self.dataCom.reset_output_buffer()

    # REF : UARTParser.sendCfg
    def uartSendCfg(self, cfg: list[str]):
        # remove empty lines from the cfg
        cfg = [line for line in cfg if line != '\n']
        # attach \n at the end of each line
        cfg = [line + '\n' if not line.endswith('\n') else line for line in cfg]
        # remove commented lines
        cfg = [line for line in cfg if line[0] != '%']

        for line in cfg:
            time.sleep(0.03)    # line dealy

            if(self.cliCom.baudrate == 1250000):
                for char in [*line]:    # [*var] unpacks list into elements
                    time.sleep(0.001)   # char delay
                    self.cliCom.write(char.encode())
            else:
                self.cliCom.write(line.encode())

            # print ack messages
            ack = self.cliCom.readline()
            print(ack, flush=True)
            ack = self.cliCom.readline()
            print(ack, flush=True)

            splitLine = line.split()
            if(splitLine[0] == "baudRate"):
                try:
                    self.cliCom.baudrate = int(splitLine[1])
                except:
                    sys.exit(1)
        
        time.sleep(0.03)
        self.cliCom.reset_input_buffer()

    def sendLine(self, line: str):
        if(self.cliCom.baudrate == 1250000):
            for char in [*line]:
                time.sleep(0.001)
                self.cliCom.write(char.encode())
        else:
            self.cliCom.write(line.encode())
        ack = self.cliCom.readline()
        print(ack)
        ack = self.cliCom.readline()
        print(ack)


class parseUartThread(QThread):
    fin = Signal(dict)

    def __init__(self, uParser: UARTParser):
            QThread.__init__(self)
            self.parser = uParser

    def run(self):
        outputDict = self.parser.readAndParseUartCOMPort()
        self.fin.emit(outputDict)

    def stop(self):
        self.terminate()


# TODO consider use or not
class PeopleTracking():
    def __init__(self):
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = Window(title="Batch Maker : Fall Detect")
    main.show()
    sys.exit(app.exec_())


# TODO in Uartsendcfg, consecutive b'' check failure and show warning window
# you have to push physical reset button