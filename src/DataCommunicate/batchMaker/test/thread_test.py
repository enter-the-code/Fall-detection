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
import time
import sys, os

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

class Work():
    def __init__(self):
        self.print_thread = PrintThread()

        self.print_thread.fin.connect(self.print_call)
        self.timer = QTimer()
        self.timer.setSingleShot(False)
        self.timer.timeout.connect(self.print_call)

    def print_call(self):
        if not self.print_thread.isRunning():
            self.print_thread.start(priority=QThread.HighestPriority)

    def start_call(self):
        self.timer.start(1000)

class PrintThread(QThread):
    fin = Signal(dict)

    def __init__(self):
            QThread.__init__(self)

    def run(self):
        print("run")
        self.fin.emit({})
        print("finish")

    def stop(self):
        self.terminate()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main = Window()
    main.show()
    myWork = Work()
    myWork.start_call()

    sys.exit(app.exec_())