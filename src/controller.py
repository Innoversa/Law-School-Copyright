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
from multiprocessing import Process, Queue
import pandas as pd
from modules.process_progress_monitor import monitor_process_progress
class controller(QMainWindow, UiWrapper):
    def __init__(self, parent=None):
        super(controller, self).__init__(parent)
        self.initialize_Ui()
        self.connect_logic_signals()
        self.threadpool = QThreadPool()
        self.is_running_multiple=False
        self.percentages=[-1,-1]
        #self.color_change_flag=[True]

    def connect_logic_signals(self):
        self.start_button.clicked.connect(self.slot_start_button_clicked)

    def test_func(self,progress_callback):
        for i in range(20):
            time.sleep(1)
            progress_callback.emit((i+1) * 5)
        return None

    def book_progress_callback(self,info_in):
        print(info_in)
        if isinstance(info_in,int):
            self.update_progress_bar(info_in)
        else:
            print('bpc',info_in)
            QMessageBox.information(self, 'Error', 'Info: ' + str(info_in))

    def thread_finished(self):
        self.clear_percentage_history()
        self.change_color_worker([138, 201, 38])
        #time.sleep(1)
        QMessageBox.information(self, 'Info', 'Scraping Finished.')

    def empty_callback(self):
        pass

    def clear_percentage_history(self):
        self.percentages=[-1,-1]

    def update_progress(self,scraper_type,percentage):
        if scraper_type=='Youtube':
            self.percentages[0]=percentage
        elif scraper_type=='Last.fm':
            self.percentages[1]=percentage

        result=0
        count=0
        for i in self.percentages:
            if i>-1:
                result+=i
                count+=1
        self.update_progress_bar(int(result/count))

    def yt_update_progress_bar(self, percentage):
        self.update_progress('Youtube',percentage)

    def lastfm_update_progress_bar(self, percentage):
        self.update_progress('Last.fm',percentage)

    def error_pop_up(self,error_info):
        print(error_info)
        self.change_color_worker([255, 0, 0])
        #time.sleep(1)
        self.clear_percentage_history()
        QMessageBox.warning(self, 'Error', 'Error: '+str(error_info[0])+str(error_info[1]))

    def change_color_worker(self,target_color):
        #self.color_change_flag[0]=True
        worker_color = Worker(self.change_color, target_color)
        worker_color.signals.result.connect(self.empty_callback)
        worker_color.signals.finished.connect(self.empty_callback)
        worker_color.signals.progress.connect(self.empty_callback)
        worker_color.signals.error.connect(self.error_pop_up)
        self.threadpool.start(worker_color)

    def slot_start_button_clicked(self):
        # self.change_color_worker([255,159,28])
        # return

        # df_dict = read_spreadsheet('sample_data\\bk.xlsm')
        # progress_queue = Queue()
        # p = Process(target=start_crawler, args=(df_dict, 'sample_data', progress_queue))
        # p.start()
        # print('p')
        # worker_monitor = Worker(monitor_process_progress,  progress_queue)
        # worker_monitor.signals.result.connect(self.empty_callback)
        # worker_monitor.signals.finished.connect(self.empty_callback)
        # worker_monitor.signals.progress.connect( self.book_progress_callback)
        # worker_monitor.signals.error.connect(self.error_pop_up)
        # self.threadpool.start(worker_monitor)
        # return

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
            self.change_color_worker([255, 159, 28])
            #time.sleep(1)
            df_dict=read_spreadsheet(self.get_all_input_information()['input_file_path'])
            if ui_input['type']=='books':
                #os.system(r'cd amazon_books_scrape\amazonscrap\ & scrapy crawl book-scraper')
                #kw={'ttr':'asd', 'progress_callback':}
                progress_queue=Queue()
                p = Process(target=start_crawler, args=(df_dict, ui_input['output_file_path'],progress_queue))
                p.start()
                worker_monitor = Worker(monitor_process_progress, progress_queue)
                worker_monitor.signals.result.connect(self.empty_callback)
                worker_monitor.signals.finished.connect(self.thread_finished)
                worker_monitor.signals.progress.connect(self.update_progress_bar)
                worker_monitor.signals.error.connect(self.error_pop_up)
                self.threadpool.start(worker_monitor)
                #self.update_progress_bar(100)
                #p.join()
            elif ui_input['type']=='songs':
                if 'Youtube' in ui_input['sources']:
                    print('youtube')
                    worker_yt = Worker(get_youtube_data, df_dict, ui_input['output_file_path'])
                    worker_yt.signals.result.connect(self.empty_callback)
                    worker_yt.signals.finished.connect(self.thread_finished)
                    worker_yt.signals.progress.connect(self.update_progress_bar)
                    worker_yt.signals.error.connect(self.error_pop_up)
                    self.threadpool.start(worker_yt)
                if 'Last.fm' in ui_input['sources']:
                    print('last.fm')
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
        if ui_input['sources']==[]:
            QMessageBox.warning(self, 'Error', "Please select scraping source.")
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
        # result['attributes']=[]
        # if self.attribute_checkBox_1.isChecked():
        #     result['sources'].append(self.widget_titles[result['type']]['attributes'][0])
        # if self.attribute_checkBox_2.isChecked():
        #     result['sources'].append(self.widget_titles[result['type']]['attributes'][1])
        # if self.attribute_checkBox_3.isChecked():
        #     result['sources'].append(self.widget_titles[result['type']]['attributes'][2])
        # if self.attribute_checkBox_4.isChecked():
        #     result['sources'].append(self.widget_titles[result['type']]['attributes'][3])

        return result
