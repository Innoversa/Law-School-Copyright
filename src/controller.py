from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from ui.qtsrc.ui_wrapper import UiWrapper
from modules.spreadsheet_reader import read_spreadsheet
import sys
import time
import os
from modules.thread_worker import Worker
from yt_scrape.myYT import get_youtube_data
from amazon_books_scrape.amazonscrap.spiders.book_scrapper import start_crawler
from last_fm.last_fm_main import perform_last_fm_s
from multiprocessing import Process
import pandas as pd

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

    def thread_finished(self):
        QMessageBox.information(self, 'Info', 'Scraping Finished.')

    def empty_callback(self):
        pass

    def error_pop_up(self,error_info):
        print(error_info)
        QMessageBox.warning(self, 'Error', 'Error: '+str(error_info[0])+str(error_info[1]))

    def slot_start_button_clicked(self):

        # df_dict = read_spreadsheet('sample_data\\bklong.xlsm')
        # p = Process(target=start_crawler, args=(df_dict, 'sample_data', None))
        # p.start()

        # print('Start Clicked')
        # df_dict = read_spreadsheet('sample_data\\songs.xlsx')
        # worker_fm = Worker(perform_last_fm_s, df_dict,'')
        # worker_fm.signals.result.connect(self.empty_callback)
        # worker_fm.signals.finished.connect(self.thread_finished)
        # worker_fm.signals.progress.connect(self.update_progress_bar)
        # worker_fm.signals.error.connect(self.error_pop_up)
        # self.threadpool.start(worker_fm)
        # return

        self.update_progress_bar(0)
        ui_input=self.get_all_input_information()
        print(ui_input)
        if self.validate_input_info(ui_input):
            df_dict=read_spreadsheet(self.get_all_input_information()['input_file_path'])
            if ui_input['type']=='books':
                #os.system(r'cd amazon_books_scrape\amazonscrap\ & scrapy crawl book-scraper')
                #kw={'ttr':'asd', 'progress_callback':}
                p = Process(target=start_crawler, args=(df_dict, ui_input['output_file_path'],None))
                p.start()

                self.update_progress_bar(100)
                #p.join()
                # try:
                #     start_crawler(None)
                # except Exception as e:
                #     print(e)
                # worker = Worker(start_crawler)
                # worker.signals.result.connect(self.print_output)
                # worker.signals.finished.connect(self.thread_finished)
                # worker.signals.progress.connect(self.update_progress_bar)
                # self.threadpool.start(worker)
            elif ui_input['type']=='songs':
                if 'Youtube' in ui_input['sources']:
                    print('youtube')
                    #TODO
                    worker_yt = Worker(get_youtube_data, df_dict, ui_input['output_file_path'])
                    worker_yt.signals.result.connect(self.empty_callback)
                    worker_yt.signals.finished.connect(self.thread_finished)
                    worker_yt.signals.progress.connect(self.update_progress_bar)
                    worker_yt.signals.error.connect(self.error_pop_up)
                    self.threadpool.start(worker_yt)
                if 'Spotify' in ui_input['sources']:
                    print('spotify')
                    worker_fm = Worker(perform_last_fm_s, df_dict, ui_input['output_file_path'])
                    worker_fm.signals.result.connect(self.empty_callback) # handled by scraper itself
                    worker_fm.signals.finished.connect(self.thread_finished)
                    worker_fm.signals.progress.connect(self.update_progress_bar)
                    worker_fm.signals.error.connect(self.error_pop_up)
                    self.threadpool.start(worker_fm)

    def test_worker(self,progress_callback):
        for i in range(0,10):
            time.sleep(1)
            progress_callback.emit((i+1)*10)

    def validate_input_info(self,ui_input):
        if not os.path.isfile(ui_input['input_file_path']):
            QMessageBox.warning(self, 'Error', "Input file is not selected or not valid.")
            return False
        if not os.path.isdir(ui_input['output_file_path']):
            QMessageBox.warning(self, 'Error', "Output path is not selected or not valid.")
            return False
        return True

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
        result['output_file_path']=self.output_path_label.text()
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
