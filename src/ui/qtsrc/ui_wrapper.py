import os
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *
from ui.qtsrc.main_window import Ui_MainWindow
from PyQt5.QtWidgets import QFileDialog

class UiWrapper(Ui_MainWindow):
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
        self.attribute_checkBox_1.setText(_translate("MainWindow", self.widget_titles['books']['attributes'][0]))
        self.attribute_checkBox_2.setText(_translate("MainWindow", self.widget_titles['books']['attributes'][1]))
        self.attribute_checkBox_3.setText(_translate("MainWindow", self.widget_titles['books']['attributes'][2]))
        self.attribute_checkBox_4.setText(_translate("MainWindow", self.widget_titles['books']['attributes'][3]))
        self.source_checkBox_1.setText(_translate("MainWindow", self.widget_titles['books']['sources'][0]))
        self.source_checkBox_2.setText(_translate("MainWindow", self.widget_titles['books']['sources'][1]))

    def songsUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.attribute_checkBox_1.setText(_translate("MainWindow", self.widget_titles['songs']['attributes'][0]))
        self.attribute_checkBox_2.setText(_translate("MainWindow", self.widget_titles['songs']['attributes'][1]))
        self.attribute_checkBox_3.setText(_translate("MainWindow", self.widget_titles['songs']['attributes'][2]))
        self.attribute_checkBox_4.setText(_translate("MainWindow", self.widget_titles['songs']['attributes'][3]))
        self.source_checkBox_1.setText(_translate("MainWindow", self.widget_titles['songs']['sources'][0]))
        self.source_checkBox_2.setText(_translate("MainWindow", self.widget_titles['songs']['sources'][1]))

    def set_button_group(self):
        self.type_button_group = QtWidgets.QButtonGroup()
        self.type_button_group.addButton(self.books_radio,0)
        self.type_button_group.addButton(self.songs_radio,1)

        self.source_button_group = QtWidgets.QButtonGroup()
        self.source_button_group.addButton(self.source_checkBox_1, 0)
        self.source_button_group.addButton(self.source_checkBox_2, 1)

        self.attribute_button_group = QtWidgets.QButtonGroup()
        self.attribute_button_group.addButton(self.attribute_checkBox_1, 0)
        self.attribute_button_group.addButton(self.attribute_checkBox_2, 1)
        self.attribute_button_group.addButton(self.attribute_checkBox_3, 2)
        self.attribute_button_group.addButton(self.attribute_checkBox_4, 3)

    def initialize_Ui(self):
        self.widget_titles={
            'songs':{
                'sources':['Youtube','Spotify'],
                'attributes':['View/Play Count', 'Duration', 'Thumbs Up','Thumbs Down']
            },
            'books': {
                'sources': ['Amazon', 'Google Books'],
                'attributes': ['Paper Copy Price', 'Paper Price Variance', 'Electronic Copy Price', 'Electronic Price Variance']
            }
        }
        self.cwd=os.getcwd()
        self.setupUi(self)
        self.connect_ui_signals()
        self.songs_radio.setChecked(True)
        #self.songsUi()