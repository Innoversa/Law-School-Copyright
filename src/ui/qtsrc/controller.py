from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui.qtsrc.main_window import Ui_MainWindow
from modules.spreadsheet_reader import read_spreadsheet
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
        # For testing:
        #print(self.get_all_input_information())
        #read_spreadsheet(self.get_all_input_information()['input_file_path'])

    def get_all_input_information(self):
        """
        Get user specified information
        :return: a dictionary of all information specified by user on UI
        """
        result={}
        if self.books_radio.isChecked():
            result['type']='books'
        else:
            result['type']='songs'
        result['input_file_path']=self.input_path_label.text()
        result['sources']=[]
        if self.source_checkBox_1.isChecked():
            result['sources'].append(self.widget_titles[result['type']]['sources'][0])
        if self.source_checkBox_2.isChecked():
            result['sources'].append(self.widget_titles[result['type']]['sources'][1])
        result['attributes']=[]
        if self.attribute_checkBox_1.isChecked():
            result['sources'].append(self.widget_titles[result['type']]['attributes'][0])
        if self.attribute_checkBox_2.isChecked():
            result['sources'].append(self.widget_titles[result['type']]['attributes'][1])
        if self.attribute_checkBox_3.isChecked():
            result['sources'].append(self.widget_titles[result['type']]['attributes'][2])
        if self.attribute_checkBox_4.isChecked():
            result['sources'].append(self.widget_titles[result['type']]['attributes'][3])

        return result