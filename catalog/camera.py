# -*- coding: utf-8 -*-
"""
Created on Wed Nov  3 07:01:20 2021

@author: Harrison
"""

from imutils.video import VideoStream
import imutils
import cv2,os,urllib.request
import numpy as np
from pyzbar.pyzbar import decode


class MaskDetect(object):
    def __init__(self):
        self.vs = cv2.VideoCapture(0+cv2.CAP_DSHOW)
        self.vs.set(3,1280)
        self.vs.set(4,720)
        
    def __del__(self):
        cv2.destroyAllWindows()
        
        
    def get_barcode(self):
        try:
            item = decode(self.frame)
            if item != []:
                barcode = item[0].data
                #barcode = barcode.decode("utf-8")
            else:
                barcode = ("_No Barcode Currently Scanned").encode("utf-8")
        except:
            barcode = "_No Frame"
        return barcode
            
        
        
    def get_frame(self):
        success, self.frame = self.vs.read()
        ret, jpeg = cv2.imencode(".jpg", self.frame)
        return jpeg.tobytes()