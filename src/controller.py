from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui.qtsrc.ui_wrapper import UiWrapper
from modules.spreadsheet_reader import read_spreadsheet
import sys
import time
from modules.thread_worker import Worker

class controller(QMainWindow, UiWrapper):
    def __init__(self, parent=None):
        super(controller, self).__init__(parent)
        self.initialize_Ui()
        self.connect_logic_signals()
        self.threadpool = QThreadPool()

    def connect_logic_signals(self):
        self.start_button.clicked.connect(self.slot_start_button_clicked)

    def test_func(self,progress_callback):
        for i in range(20):
            time.sleep(1)
            progress_callback.emit((i+1) * 5)
        return None

    def print_output(self, o):
        print(o)

    def thread_finished(self):
        print("Finished")

    def slot_start_button_clicked(self):
        QMessageBox.warning(self, 'Not Implemented', "Scraping functions has not implemented yet. "
                                                     "Results are for testing only.")
        # For testing:
        #print(self.get_all_input_information())
        #read_spreadsheet(self.get_all_input_information()['input_file_path'])
        worker = Worker(self.test_func)
        worker.signals.result.connect(self.print_output)
        worker.signals.finished.connect(self.thread_finished)
        worker.signals.progress.connect(self.update_progress_bar)
        self.threadpool.start(worker)

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