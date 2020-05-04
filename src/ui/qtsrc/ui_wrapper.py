import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
#from ui.qtsrc.main_window import Ui_MainWindow
from ui.qtsrc.mainWindows_compact import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog
import time

class UiWrapper(Ui_MainWindow):
    # def __init__(self):
    #     pass
    def connect_ui_signals(self):
        self.books_radio.clicked.connect(self.slot_books_radio_clicked)
        self.songs_radio.clicked.connect(self.slot_songs_radio_clicked)
        self.browse_input_button.clicked.connect(self.slot_browse_input_button_clicked)
        self.browse_output_button.clicked.connect(self.slot_browse_output_button_clicked)

    def slot_browse_input_button_clicked(self):
        file_chosen, _ = QFileDialog.getOpenFileName(self, 'Select input file')
        if file_chosen != "":
            self.input_path_label.setText(file_chosen)

    def slot_browse_output_button_clicked(self):
        file_chosen = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        if file_chosen != "":
            self.output_path_label.setText(file_chosen)

    def slot_books_radio_clicked(self):
        self.booksUi()

    def slot_songs_radio_clicked(self):
        self.songsUi()

    def booksUi(self):
        _translate = QtCore.QCoreApplication.translate
        # self.attribute_checkBox_1.setText(_translate("MainWindow", self.widget_titles['books']['attributes'][0]))
        # self.attribute_checkBox_2.setText(_translate("MainWindow", self.widget_titles['books']['attributes'][1]))
        # self.attribute_checkBox_3.setText(_translate("MainWindow", self.widget_titles['books']['attributes'][2]))
        # self.attribute_checkBox_4.setText(_translate("MainWindow", self.widget_titles['books']['attributes'][3]))
        self.source_checkBox_1.setText(_translate("MainWindow", self.widget_titles['books']['sources'][0]))
        self.source_checkBox_2.setVisible(False)
        #self.source_checkBox_2.setText(_translate("MainWindow", self.widget_titles['books']['sources'][1]))

    def songsUi(self):
        _translate = QtCore.QCoreApplication.translate
        # self.attribute_checkBox_1.setText(_translate("MainWindow", self.widget_titles['songs']['attributes'][0]))
        # self.attribute_checkBox_2.setText(_translate("MainWindow", self.widget_titles['songs']['attributes'][1]))
        # self.attribute_checkBox_3.setText(_translate("MainWindow", self.widget_titles['songs']['attributes'][2]))
        # self.attribute_checkBox_4.setText(_translate("MainWindow", self.widget_titles['songs']['attributes'][3]))
        self.source_checkBox_1.setText(_translate("MainWindow", self.widget_titles['songs']['sources'][0]))
        self.source_checkBox_2.setVisible(True)
        self.source_checkBox_2.setText(_translate("MainWindow", self.widget_titles['songs']['sources'][1]))

    def update_progress_bar(self,percentage):
        self.progressBar.setValue(percentage)

    def set_button_group(self):
        self.type_button_group = QtWidgets.QButtonGroup()
        self.type_button_group.addButton(self.books_radio,0)
        self.type_button_group.addButton(self.songs_radio,1)

        self.source_button_group = QtWidgets.QButtonGroup()
        self.source_button_group.addButton(self.source_checkBox_1, 0)
        self.source_button_group.addButton(self.source_checkBox_2, 1)

        self.attribute_button_group = QtWidgets.QButtonGroup()
        # self.attribute_button_group.addButton(self.attribute_checkBox_1, 0)
        # self.attribute_button_group.addButton(self.attribute_checkBox_2, 1)
        # self.attribute_button_group.addButton(self.attribute_checkBox_3, 2)
        # self.attribute_button_group.addButton(self.attribute_checkBox_4, 3)

    def initialize_widget_values(self):
        self.progressBar.setValue(0)


    def initialize_Ui(self):
        self.widget_titles={
            'songs':{
                'sources':['Youtube','Last.fm'],
                'attributes':['View/Play Count', 'Duration', 'Thumbs Up','Thumbs Down']
            },
            'books': {
                'sources': ['Amazon', 'Google Books'],
                'attributes': ['Paper Copy Price', 'Paper Price Variance', 'Electronic Copy Price', 'Electronic Price Variance']
            }
        }
        self.cwd=os.getcwd()
        self.setupUi(self)
        self.initialize_widget_values()
        self.connect_ui_signals()
        self.songs_radio.setChecked(True)
        self.songsUi()
        self.current_color=[80,0,0]

    def apply_current_color(self):
        for c_pos in range(len(self.current_color)):
            if self.current_color[c_pos] >= 255:
                self.current_color[c_pos] = 253
            elif self.current_color[c_pos] < 0:
                self.current_color[c_pos] = 0
        self.left_frame.setStyleSheet("background-color: rgb(" + str(int(self.current_color[0])) + ", " + str(
            int(self.current_color[1])) + ", " + str(int(self.current_color[2])) + ");")

    def change_color(self,target_color,progress_callback):
        steps=10
        dr=(target_color[0]-self.current_color[0])/steps
        dg=(target_color[1]-self.current_color[1])/steps
        db=(target_color[2]-self.current_color[2])/steps
        for i in range(steps):
            self.current_color[0]+=dr
            self.current_color[1]+=dg
            self.current_color[2]+=db
            self.apply_current_color()
            time.sleep(0.05)

        # breathing_steps=30
        # try:
        #     while breathing and control_flag[0]:
        #         delta_brightness=2
        #         for i in range(breathing_steps):
        #             self.current_color[0]+=delta_brightness
        #             self.current_color[1]+=delta_brightness
        #             self.current_color[2]+=delta_brightness
        #             self.apply_current_color()
        #             time.sleep(0.1)
        #         delta_brightness=-1
        #         for i in range(breathing_steps):
        #             self.current_color[0] += delta_brightness
        #             self.current_color[1] += delta_brightness
        #             self.current_color[2] += delta_brightness
        #             self.apply_current_color()
        #             time.sleep(0.1)
        # except Exception as e:
        #     print(e)