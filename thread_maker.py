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
from PyQt5.QtCore import QThread, pyqtSignal
import numpy as np

class Play_thread(QThread):
    my_signal = pyqtSignal(int)
    zoom_play_signal = pyqtSignal(int)

    def __int__(self, parent=None):
        super(Play_thread, self).__init__(parent)

    def load(self, play_process):
        self.play_process = play_process
        self.max_frm_num = np.max(list(play_process.frm_num_dict.values()))

    def run(self):
        i = 0
        while True:
            while i < self.max_frm_num:
                while self.play_process.ispause:
                    if self.play_process.stop_flag:
                        i = 0
                        self.my_signal.emit(i)
                        self.zoom_play_signal.emit(i)
                    if self.play_process.pre_flag:
                        i = max(0, i - 1)
                        self.my_signal.emit(i)
                        self.zoom_play_signal.emit(i)
                        self.play_process.pre_flag = False
                    elif self.play_process.next_flag:
                        i = min(self.max_frm_num - 1, i + 1)
                        self.my_signal.emit(i)
                        self.zoom_play_signal.emit(i)
                        self.play_process.next_flag = False
                    self.msleep(30)
                self.msleep(self.play_process.ms_per_frm)
                self.my_signal.emit(i)
                self.zoom_play_signal.emit(i)
                i += 1
            i = 0

