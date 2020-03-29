# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindows.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import os

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        self.cwd=os.getcwd()
        self.MainWindow=MainWindow
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 400)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/resources/images/icon.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.left_frame = QtWidgets.QFrame(self.centralwidget)
        self.left_frame.setGeometry(QtCore.QRect(-1, -1, 201, 501))
        self.left_frame.setStyleSheet("background-color: rgb(80, 0, 0);")
        self.left_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.left_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.left_frame.setObjectName("left_frame")
        self.title_label = QtWidgets.QLabel(self.left_frame)
        self.title_label.setGeometry(QtCore.QRect(10, 20, 181, 41))
        self.title_label.setStyleSheet("font: 25 22pt \"Segoe UI Light\";")
        self.title_label.setObjectName("title_label")
        self.title_line = QtWidgets.QLabel(self.left_frame)
        self.title_line.setGeometry(QtCore.QRect(10, 40, 181, 31))
        self.title_line.setObjectName("title_line")
        self.type_group = QtWidgets.QGroupBox(self.left_frame)
        self.type_group.setGeometry(QtCore.QRect(30, 90, 151, 111))
        self.type_group.setStyleSheet("font: 25 10pt \"Segoe UI Light\";\n"
"color:rgb(255,255,255);")
        self.type_group.setObjectName("type_group")
        self.books_radio = QtWidgets.QRadioButton(self.type_group)
        self.books_radio.setGeometry(QtCore.QRect(30, 70, 82, 21))
        self.books_radio.setStyleSheet("font: 25 12pt \"Segoe UI Light\";\n"
"color:rgb(255,255,255);")
        self.books_radio.setObjectName("books_radio")
        self.songs_radio = QtWidgets.QRadioButton(self.type_group)
        self.songs_radio.setGeometry(QtCore.QRect(30, 30, 111, 21))
        self.songs_radio.setStyleSheet("font: 25 12pt \"Segoe UI Light\";\n"
"color:rgb(255,255,255);")
        self.songs_radio.setObjectName("songs_radio")
        self.title_line.raise_()
        self.title_label.raise_()
        self.type_group.raise_()
        self.right_frame = QtWidgets.QFrame(self.centralwidget)
        self.right_frame.setGeometry(QtCore.QRect(199, -1, 601, 501))
        self.right_frame.setStyleSheet("background-color: rgb(214, 210, 196);")
        self.right_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.right_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.right_frame.setObjectName("right_frame")
        self.input_label = QtWidgets.QLabel(self.right_frame)
        self.input_label.setGeometry(QtCore.QRect(30, 30, 91, 21))
        self.input_label.setStyleSheet("font: 10pt \"Segoe UI\";")
        self.input_label.setObjectName("input_label")
        self.holine = QtWidgets.QLabel(self.right_frame)
        self.holine.setGeometry(QtCore.QRect(30, 40, 561, 20))
        self.holine.setObjectName("holine")
        self.frame = QtWidgets.QFrame(self.right_frame)
        self.frame.setGeometry(QtCore.QRect(0, 120, 611, 181))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame)
        self.groupBox_2.setGeometry(QtCore.QRect(30, 110, 531, 51))
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 20, 511, 20))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.checkBox_3 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_3.setObjectName("checkBox_3")
        self.horizontalLayout.addWidget(self.checkBox_3)
        self.checkBox_4 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_4.setObjectName("checkBox_4")
        self.horizontalLayout.addWidget(self.checkBox_4)
        self.checkBox_5 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_5.setObjectName("checkBox_5")
        self.horizontalLayout.addWidget(self.checkBox_5)
        self.checkBox_6 = QtWidgets.QCheckBox(self.layoutWidget)
        self.checkBox_6.setObjectName("checkBox_6")
        self.horizontalLayout.addWidget(self.checkBox_6)
        self.groupBox = QtWidgets.QGroupBox(self.frame)
        self.groupBox.setGeometry(QtCore.QRect(30, 50, 531, 51))
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget1 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 511, 20))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.checkBox = QtWidgets.QCheckBox(self.layoutWidget1)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_2.addWidget(self.checkBox)
        self.checkBox_2 = QtWidgets.QCheckBox(self.layoutWidget1)
        self.checkBox_2.setObjectName("checkBox_2")
        self.horizontalLayout_2.addWidget(self.checkBox_2)
        self.settings_label = QtWidgets.QLabel(self.frame)
        self.settings_label.setGeometry(QtCore.QRect(30, 10, 91, 21))
        self.settings_label.setStyleSheet("font: 10pt \"Segoe UI\";")
        self.settings_label.setObjectName("settings_label")
        self.holine2 = QtWidgets.QLabel(self.frame)
        self.holine2.setGeometry(QtCore.QRect(30, 20, 561, 20))
        self.holine2.setObjectName("holine2")
        self.holine2.raise_()
        self.groupBox_2.raise_()
        self.groupBox.raise_()
        self.settings_label.raise_()
        self.input_path_label = QtWidgets.QLabel(self.right_frame)
        self.input_path_label.setGeometry(QtCore.QRect(60, 80, 301, 16))
        self.input_path_label.setObjectName("label")
        self.browse_button = QtWidgets.QPushButton(self.right_frame)
        self.browse_button.setGeometry(QtCore.QRect(420, 80, 75, 23))
        self.browse_button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.browse_button.setObjectName("browse_button")
        self.start_button = QtWidgets.QPushButton(self.right_frame)
        self.start_button.setGeometry(QtCore.QRect(420, 320, 75, 23))
        self.start_button.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.start_button.setObjectName("start_button")
        self.progressBar = QtWidgets.QProgressBar(self.right_frame)
        self.progressBar.setGeometry(QtCore.QRect(60, 320, 331, 23))
        self.progressBar.setProperty("value", 24)
        self.progressBar.setObjectName("progressBar")
        self.holine.raise_()
        self.input_label.raise_()
        self.frame.raise_()
        self.input_path_label.raise_()
        self.browse_button.raise_()
        self.start_button.raise_()
        self.progressBar.raise_()
        MainWindow.setCentralWidget(self.centralwidget)
        self.connect_ui_signals()
        self.retranslateUi(MainWindow)
        self.songs_radio.setChecked(True)
        self.songsUi()
        QtCore.QMetaObject.connectSlotsByName(MainWindow)
        #self.set_button_group()
    def connect_ui_signals(self):
        self.books_radio.clicked.connect(self.slot_books_radio_clicked)
        self.songs_radio.clicked.connect(self.slot_songs_radio_clicked)
        self.browse_button.clicked.connect(self.slot_select_button_clicked)

    def slot_select_button_clicked(self):
        file_chosen, _ = QFileDialog.getOpenFileName(self, 'Select input file')
        if file_chosen != "":
            self.input_path_label.setText(file_chosen)

    def slot_books_radio_clicked(self):
        self.booksUi()

    def slot_songs_radio_clicked(self):
        self.songsUi()

    def set_button_group(self):
        self.type_button_group = QtWidgets.QButtonGroup()
        self.type_button_group.addButton(self.books_radio,0)
        self.type_button_group.addButton(self.songs_radio,1)

        self.source_button_group = QtWidgets.QButtonGroup()
        self.source_button_group.addButton(self.checkBox,0)
        self.source_button_group.addButton(self.checkBox_2,1)

        self.attribute_button_group = QtWidgets.QButtonGroup()
        self.attribute_button_group.addButton(self.checkBox_3,0)
        self.attribute_button_group.addButton(self.checkBox_4,1)
        self.attribute_button_group.addButton(self.checkBox_5,2)
        self.attribute_button_group.addButton(self.checkBox_6,3)

    def booksUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.groupBox_2.setTitle(_translate("MainWindow", "Scraping Attributes"))
        self.checkBox_3.setText(_translate("MainWindow", "Paper Copy Price"))
        self.checkBox_4.setText(_translate("MainWindow", "Paper Price Variance"))
        self.checkBox_5.setText(_translate("MainWindow", "Electronic Copy Price"))
        self.checkBox_6.setText(_translate("MainWindow", "Electronic Price Variance"))
        self.groupBox.setTitle(_translate("MainWindow", "Scraping Source"))
        self.checkBox.setText(_translate("MainWindow", "Amazon"))
        self.checkBox_2.setText(_translate("MainWindow", "Google Books"))

    def songsUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.groupBox_2.setTitle(_translate("MainWindow", "Scraping Attributes"))
        self.checkBox_3.setText(_translate("MainWindow", "View/Play Count"))
        self.checkBox_4.setText(_translate("MainWindow", "Duration"))
        self.checkBox_5.setText(_translate("MainWindow", "Thumbs Up"))
        self.checkBox_6.setText(_translate("MainWindow", "Thumbs Down"))
        self.groupBox.setTitle(_translate("MainWindow", "Scraping Source"))
        self.checkBox.setText(_translate("MainWindow", "Youtube"))
        self.checkBox_2.setText(_translate("MainWindow", "Spotify"))

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Data Scraper"))
        self.title_label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" color:#ffffff;\">Data Scraper</span></p></body></html>"))
        self.title_line.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:18pt; font-weight:600; color:#ffffff;\">_________________</span></p></body></html>"))
        self.type_group.setTitle(_translate("MainWindow", "Type"))
        self.books_radio.setText(_translate("MainWindow", "Books"))
        self.songs_radio.setText(_translate("MainWindow", "Songs"))
        self.input_label.setText(_translate("MainWindow", "Input"))
        self.holine.setText(_translate("MainWindow", "__________________________________________________________________________________________"))
        self.settings_label.setText(_translate("MainWindow", "Settings"))
        self.holine2.setText(_translate("MainWindow", "__________________________________________________________________________________________"))
        self.input_path_label.setText(_translate("MainWindow", "Please select input xlsx file... No file chosen yet."))
        self.browse_button.setText(_translate("MainWindow", "Browse.."))
        self.start_button.setText(_translate("MainWindow", "Start"))

    def get_current_values(self):
        pass
import ui.qtsrc.resources_rc
import sys
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())