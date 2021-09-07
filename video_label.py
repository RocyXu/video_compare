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
from PyQt5.QtWidgets import QLabel
from PyQt5.QtGui import QMouseEvent, QPaintEvent, QPainter, QPen
from PyQt5.QtCore import QRect, Qt, pyqtSignal

class Video_label(QLabel):
    zoom_signal = pyqtSignal(list)

    def __init__(self, parent=None):
        super(Video_label, self).__init__(parent)
        self.press_flag = False
        self.rect = []

    def mousePressEvent(self, ev: QMouseEvent) -> None:
        self.lt_x, self.lt_y = ev.x(), ev.y()
        self.rb_x, self.rb_y = ev.x(), ev.y()
        self.press_flag = True
        #return super().mousePressEvent(ev)

    def mouseMoveEvent(self, ev: QMouseEvent) -> None:
        if self.press_flag:
            self.rb_x, self.rb_y = ev.x(), ev.y()
            self.update()
        #return super().mouseMoveEvent(ev)

    def mouseReleaseEvent(self, ev: QMouseEvent) -> None:
        self.press_flag = False
        self.update()

        if abs(self.rb_x - self.lt_x) > 50 and abs(self.rb_y - self.lt_y) > 50:
            self.rect = [self.lt_x, self.lt_y, abs(self.rb_x - self.lt_x), abs(self.rb_y - self.lt_y)]
            self.zoom_signal.emit(self.rect)
        #return super().mouseReleaseEvent(ev)
    
    def paintEvent(self, a0: QPaintEvent) -> None:
        super().paintEvent(a0)
        if self.press_flag:
            try:
                painter = QPainter(self)
                painter.setPen(QPen(Qt.red, 2, Qt.SolidLine))
                rect = QRect(self.lt_x, self.lt_y, abs(self.rb_x - self.lt_x), abs(self.rb_y - self.lt_y))
                painter.drawRect(rect)
            except AttributeError:
                pass
        else:
            try:
                painter = QPainter(self)
                painter.setPen(QPen(Qt.green, 2, Qt.SolidLine))
                rect = QRect(self.lt_x, self.lt_y, abs(self.rb_x - self.lt_x), abs(self.rb_y - self.lt_y))
                painter.drawRect(rect)
            except AttributeError:
                pass
        #return super().paintEvent(a0)