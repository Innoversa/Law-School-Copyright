from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui.qtsrc.mainWindows import Ui_MainWindow
import sys

class controller(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(controller, self).__init__(parent)
        self.setupUi(self)
        self.connect_logic_signals()
    def connect_logic_signals(self):
        self.start_button.clicked.connect(self.slot_start_button_clicked)

    def slot_start_button_clicked(self):
        QMessageBox.warning(self, 'Not Implemented', "Scraping functions has not implemented yet.")
