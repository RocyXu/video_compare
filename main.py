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
import sys

from main_window import *
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget
from read_operators import File_parser
from play_controller import *

import cv2

TASK_BAR_HEIGHT = 70 / 1080
MAX_WIN_NUM = 4

class MyMainWindow(QWidget, Ui_Form):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.setupUi(self)

        ### main win style
        self.main_win_style()

        ### for file parsing
        self.file_parser = File_parser(filer_keys=['.mp4'])
        self.file_list = None

        ### for play controlling
        self.player = Play_process(self)

        # for speed conttrolling
        self.speed_ctrl = Speed_controller(self.lineEdit, self)

        # for win creating
        self.win_ctrl = Window_controller(
            self.full_w, self.full_h * (1 - TASK_BAR_HEIGHT), self)

        ### buttons signals connect
        self.pushButton.setShortcut('q')
        self.pushButton_3.setShortcut('w')
        self.pushButton_4.setShortcut('e')
        self.pushButton_5.setShortcut('r')

        self.clear_button_ctrl = Clear_Button_controller(self.pushButton_6, self)
        self.play_button_ctrl = Play_Button_controller(self.pushButton, self)
        self.pre_button_ctrl = Pre_Button_controller(self.pushButton_4, self)
        self.next_button_ctrl = Next_Button_controller(self.pushButton_5, self)
        self.stop_button_ctrl = Stop_Button_controller(self.pushButton_3, self)

        self.isplaying = False

    def main_win_style(self):
        desktop = QApplication.desktop().screenGeometry(0)
        self.full_w = desktop.width()
        self.full_h = desktop.height()
        win_w = self.width()
        win_h = self.height()
        self.setFixedSize(self.width(), self.height())
        self.setAcceptDrops(True)
        self.lineEdit.setEnabled(False)
        self.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
        self.setFocusPolicy(QtCore.Qt.StrongFocus)
        ### move
        self.move(
            int(self.full_w - win_w), 
            int(self.full_h - win_h - TASK_BAR_HEIGHT * self.full_h))

    def dragEnterEvent(self, a0: QtGui.QDragEnterEvent) -> None:
        a0.accept()

    def dropEvent(self, a0: QtGui.QDropEvent) -> None:
        accpted_string = a0.mimeData().text()
        self.video_caps_dict = self.file_parser(accpted_string).decode_videos()

        if not self.video_caps_dict:
            QMessageBox.critical(self,"ERROR","非mp4拖了个寂寞！",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            return
        if len(self.video_caps_dict.keys()) > MAX_WIN_NUM:
            QMessageBox.critical(self,"ERROR","4不4！",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            return

        ### allowed to change speed
        self.lineEdit.setEnabled(True)
        ### create namedwindow
        self.win_ctrl.create_wins(self.video_caps_dict.keys())
        self.win_ctrl.show()
        # for play processing
        self.player.load_frm(self.video_caps_dict)
        self.player.show(self.win_ctrl)
        if not self.isplaying:
            self.player.start_play_thread()
            self.isplaying = True
        ### show

    def restart(self):
        self.video_caps_dict = None
        self.win_ctrl.destroy()

    def closeEvent(self,event):
        self.win_ctrl.close()
        self.close()

    def __del__(self):
        print("quit")
        self.win_ctrl.close()
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    myWin = MyMainWindow()
    myWin.show()
    sys.exit(app.exec_())


