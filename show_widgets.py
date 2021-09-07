# -*- coding: utf-8 -*- #
# ------------------------------------------------------------------
# File Name:        
# Author: xurongxin
# Version:          
# Created:          
# Description:  
# Function List:    
# History:
#       <author>        <version>       <time>      <desc>
# ------------------------------------------------------------------
from PyQt5.QtWidgets import QLabel, QPushButton, QWidget, QApplication, QGraphicsScene, QGraphicsPixmapItem, QVBoxLayout
from PyQt5.QtGui import  QImage, QPixmap
from PyQt5 import QtCore
from video_widget import Ui_Form
import cv2

class Video_widget(QWidget, Ui_Form):
    def __init__(self, title, w, h, position, main_win_obj, parent=None):
        super(Video_widget, self).__init__(parent)
        self.setupUi(self) 

        self.resize(w, h)
        self.move(position[0], position[1])
        self.setWindowTitle(title)
        self.setFixedSize(self.width(), self.height())
        self.label.setGeometry(QtCore.QRect(-1, -1, self.width(), self.height()))
        self.label.zoom_signal.connect(main_win_obj.win_ctrl.create_zoom_win)
        self.label.zoom_signal.connect(main_win_obj.player.catch_rect)

    def add_image(self, BGR):
        h, w, _ = BGR.shape
        bytesPerLine = 3 * w
        RGB = cv2.cvtColor(BGR, cv2.COLOR_BGR2RGB)
        self.img = QImage(RGB.data, w, h, bytesPerLine, QImage.Format_RGB888)
        self.pix = QPixmap(self.img).scaled(self.label.size())
        self.label.setPixmap(self.pix)
        #QApplication.processEvents() ### !!!!
        #print("add_image")

class ZoomVideo_widget(QWidget):
    def __init__(self, title, w, h, position, parent=None):
        super(ZoomVideo_widget, self).__init__(parent)
        self.resize(w, h)
        self.move(position[0], position[1])
        self.setWindowTitle(title)
        self.setFixedSize(self.width(), self.height())
        self.label = QLabel(self)
        self.label.setGeometry(QtCore.QRect(-1, -1, self.width(), self.height()))

        self.text1 = QLabel(self)
        self.text1.setGeometry(QtCore.QRect(5, 5, self.width() // 2, 10))
        self.text1.setStyleSheet("color:gold")
        self.text2 = QLabel(self)
        self.text2.setGeometry(QtCore.QRect(self.width() // 2, 5, self.width() // 2, 10))
        self.text2.setStyleSheet("color:gold")
        self.text3 = QLabel(self)
        self.text3.setGeometry(QtCore.QRect(5, self.height() - 15, self.width() // 2, 10))
        self.text3.setStyleSheet("color:gold")
        self.text4 = QLabel(self)
        self.text4.setGeometry(QtCore.QRect(self.width() // 2, self.height() - 15, self.width() // 2, 10))
        self.text4.setStyleSheet("color:gold")

        self.label.lower()

    def add_image(self, BGR):
        h, w, c = BGR.shape
        bytesPerLine = 3 * w
        RGB = cv2.cvtColor(BGR, cv2.COLOR_BGR2RGB)
        self.img = QImage(RGB.data, w, h, bytesPerLine, QImage.Format_RGB888)
        self.pix = QPixmap(self.img).scaled(self.label.size())
        self.label.setPixmap(self.pix)
        #QApplication.processEvents() ### !!!!
        #print("add_image")