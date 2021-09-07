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
import sys, abc
import cv2
from PyQt5.QtWidgets import QMessageBox
import threading
import collections

from main_window import *
from show_widgets import Video_widget, ZoomVideo_widget
from thread_maker import *
import numpy as np


class Speed_controller():
    def __init__(self, obj, win_obj) -> None:
        self.obj = obj # obj is instance of QLineEdit
        self._text = None
        self.connect_signals()
        self.win_obj = win_obj

    def connect_signals(self):
        self.obj.returnPressed.connect(self.enter_press)
    
    def enter_press(self):
        self._text = self.obj.text()
        
        times = float(self._text)
        self.win_obj.player.ms_per_frm = 30 *(1 / times)
        self.obj.clearFocus()
    
    @property
    def text(self):
        return self._text 

class Window_controller():
    def __init__(self, desk_w, desk_h, main_win_obj) -> None:
        self.desk_w, self.desk_h = desk_w, desk_h
        self.win_list = []
        self.video_widgets = {}
        self.main_win_obj = main_win_obj

    def create_wins(self, win_list):
        self.win_list = win_list
        win_num = len(win_list)
        w, h = int(self.desk_w // 2), int(self.desk_h // 2)
        for i, win in enumerate(win_list):
            wid = Video_widget(win, w, h, ((i % 2) * w, (i // 2) * h), self.main_win_obj)
            self.video_widgets[win] = wid

        self.video_win_w = w
        self.video_win_h = h

        print("create_zoom_win")
        self.zoom_win = ZoomVideo_widget("zoom", self.desk_w * 0.85, self.desk_h * 0.85, (0, 0))

    def create_zoom_win(self):
        self.zoom_win.show()

    def show(self):
        for wid in self.video_widgets.values():
            wid.show()

    def close(self):
        for wid in self.video_widgets.values():
            wid.close()
        self.zoom_win.close()

    def destroy(self):
        for win in self.win_list:
            cv2.destroyWindow(win)
    
    def __del__(self):
        print("Window_controller quit")

class Button_controller():
    def __init__(self, obj) -> None:
        self.obj = obj # obj is instance of QLineEdit
        self.connect_signals()

    def connect_signals(self):
        self.obj.clicked.connect(self.clicked)
    
    def clicked(self):
        pass

class Stop_Button_controller(Button_controller):
    def __init__(self, obj, win_obj) -> None:
        super(Stop_Button_controller, self).__init__(obj)
        self.win_obj = win_obj
        
    def clicked(self):
        if self.win_obj.player.ispause:
            self.win_obj.player.stop_flag = True
        else:
            QMessageBox.critical(self.win_obj,"ERROR","Pause then Stop！",QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
            

class Pre_Button_controller(Button_controller):
    def __init__(self, obj, win_obj) -> None:
        super(Pre_Button_controller, self).__init__(obj)
        self.win_obj = win_obj
        
    def clicked(self):
        if self.win_obj.player.ispause:
            self.win_obj.player.pre_flag = True

class Next_Button_controller(Button_controller):
    def __init__(self, obj, win_obj) -> None:
        super(Next_Button_controller, self).__init__(obj)
        self.win_obj = win_obj
        
    def clicked(self):
        if self.win_obj.player.ispause:
            self.win_obj.player.next_flag = True


class Clear_Button_controller(Button_controller):
    def __init__(self, obj, win_obj) -> None:
        super(Clear_Button_controller, self).__init__(obj)
        self.win_obj = win_obj
        
    def clicked(self):
        self.win_obj.restart()

class Play_Button_controller(Button_controller):
    def __init__(self, obj, win_obj) -> None:
        super(Play_Button_controller, self).__init__(obj)
        self.win_obj = win_obj

        self.isplaying = False
        
    def clicked(self): # flag is processed in Play_thread
        if not self.isplaying:
            self.win_obj.player.start_play_thread()
            self.isplaying = True
        if self.win_obj.player.ispause:
            self.win_obj.player.ispause = False
            self.win_obj.player.stop_flag = False
        else:
            self.win_obj.player.ispause = True

def load_thread_fun(play_processer, win_name):
    cap = play_processer.video_caps_dict[win_name]
    play_processer.frm_num_dict[win_name] = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    while True:
        ret, img = cap.read()
        if not ret:
            break
        play_processer.video_frm_dict[win_name].append(img)

class Play_process():
    def __init__(self, win_obj) -> None:
        self.ispause = True
        self.pre_flag = False
        self.next_flag = False
        self.stop_flag = False
        self.ms_per_frm = 30

        self.main_win = win_obj

        self.isdelete = False
        self.video_frm_dict = collections.defaultdict(list)
        self.frm_num_dict = collections.defaultdict(int)
        self.cur_idx = 0
        ### init img
    def load_frm(self, video_caps_dict):
        self.video_caps_dict = video_caps_dict
        ### load frms
        p_list = []
        for win_name in self.video_caps_dict.keys():
            p = threading.Thread(target=load_thread_fun, args=(self, win_name,))
            p.start()
            p_list.append(p)
        for p in p_list:
            p.join()

    def start_play_thread(self):
        self.play_thread = Play_thread()
        self.play_thread.load(play_process=self)
        self.play_thread.my_signal.connect(self.play_pause)
        self.play_thread.zoom_play_signal.connect(self.show_zoom)
        self.play_thread.start()

    def show(self, win_ctrl=None, idx=0):
        ##### move to thread
        if win_ctrl is not None:
            self.win_ctrl = win_ctrl
        for win_name, cap in self.video_frm_dict.items():
            id_tmp = min(len(cap) - 1, idx)
            self.win_ctrl.video_widgets[win_name].add_image(cap[id_tmp])
    
    def show_zoom(self, idx):
        ### crop and merge !!!!!!!!!!!!!!!!!!!!!!
        # pass
        zoom_win = self.main_win.win_ctrl.zoom_win
        w_label, h_label = zoom_win.label.width(), zoom_win.label.height()
        merge_img = np.zeros((h_label, w_label, 3), dtype=np.uint8)

        ### crop from video_frm_dict
        video_num = len(self.video_frm_dict.keys())
        caps = list(self.video_frm_dict.values())
        keys = list(self.video_frm_dict.keys())
        try:
            x, y, w, h = self.zoom_rect
        except:
            return
        win_w, win_h = self.main_win.win_ctrl.video_win_w, self.main_win.win_ctrl.video_win_h
        BGR_h, BGR_w, c = caps[0][0].shape
        x, y, w, h = int(x / win_w * BGR_w), int(y / win_h * BGR_h), int(w / win_w * BGR_w), int(h / win_h * BGR_h)

        if video_num == 1:
            id_tmp = min(len(caps[0]) - 1, idx)
            merge_crop = np.zeros((h, w, 3), dtype=np.uint8)
            merge_crop = caps[0][id_tmp][y:y + h, x:x + w, :]
            zoom_win.text1.setText(keys[0])

        elif video_num == 2:
            merge_crop = np.zeros((h, w * 2, 3), dtype=np.uint8)
            id_tmp = min(len(caps[0]) - 1, idx)
            merge_crop[:, :w, :] = caps[0][id_tmp][y:y + h, x:x + w, :]
            id_tmp = min(len(caps[1]) - 1, idx)
            merge_crop[:, w:, :] = caps[1][id_tmp][y:y + h, x:x + w, :]

            zoom_win.text1.setText(keys[0])
            zoom_win.text2.setText(keys[1])
        else:
            merge_crop = np.zeros((h * 2, w * 2, 3), dtype=np.uint8)
            id_tmp = min(len(caps[0]) - 1, idx)
            merge_crop[:h, :w, :] = caps[0][id_tmp][y:y + h, x:x + w, :]
            id_tmp = min(len(caps[1]) - 1, idx)
            merge_crop[:h, w:, :] = caps[1][id_tmp][y:y + h, x:x + w, :]
            id_tmp = min(len(caps[2]) - 1, idx)
            merge_crop[h:, :w, :] = caps[2][id_tmp][y:y + h, x:x + w, :]
            zoom_win.text1.setText(keys[0])
            zoom_win.text2.setText(keys[1])
            zoom_win.text3.setText(keys[2])

            try:
                id_tmp = min(len(caps[3]) - 1, idx)
                merge_crop[h:, w:, :] = caps[3][id_tmp][y:y + h, x:x + w, :]
                zoom_win.text4.setText(keys[3])
            except:
                pass

        crop_h, crop_w, c = merge_crop.shape
        zoom_times = min(w_label / crop_w, h_label / crop_h)
        crop_h, crop_w = int(zoom_times * crop_h), int(zoom_times * crop_w)

        merge_crop = cv2.resize(merge_crop, (crop_w, crop_h), interpolation=cv2.INTER_CUBIC)
        lt_y = (h_label - crop_h) // 2
        lt_x = (w_label - crop_w) // 2
        merge_img[lt_y:lt_y + crop_h, lt_x:lt_x + crop_w, :] = merge_crop

        zoom_win.add_image(merge_img)
        # for win_name, cap in self.video_frm_dict.items():
        #     self.win_ctrl.video_widgets[win_name].add_image(cap[idx])
    
    def play_pause(self, cur_idx):
        self.show(idx=cur_idx)
    
    def catch_rect(self, draw_rect):
        self.zoom_rect = draw_rect
        self.show_zoom(idx=self.cur_idx)

    def __del__(self):
        self.isdelete = True
        print("Player process quit")
    



