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
import os, glob
import threading
import cv2
import numpy as np

# def read_video_to_img(parser, video_file, idx):
#     #parser.frm
#     cap = cv2.VideoCapture(video_file)
#     frm_nums = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
#     w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     all_frms = np.zeros((frm_nums, h, w, 3), dtype=np.uint8)
#
#     for i in range(frm_nums):
#         ret, f = cap.read()
#         all_frms[i, :, :, :] = f
#     parser.video_datas[idx] = all_frms

class File_parser():
    def __init__(self, filer_keys=['.mp4']) -> None:
        self.filer_key = filer_keys
        self.video_captures = {}

    def _isOk(self, item):
        for key in self.filer_key:
            if key in item:
                return True
        return False

    def __call__(self, in_strings):
        files = in_strings.replace("file:///", '')
        file_list = files.split('\n')
        self.file_list = [i for i in file_list if self._isOk(i)]

        return self

    def decode_videos(self):
        """Encode value into uint8 feature
        Returns:
            opencv video captures.
        """
        for i in range(len(self.file_list)):
            splits = os.path.split(self.file_list[i])
            basename = os.path.basename(splits[0])
            cap = cv2.VideoCapture(self.file_list[i])
            self.video_captures["{}_{}".format(basename, splits[1])] = cap
        
        return self.video_captures





