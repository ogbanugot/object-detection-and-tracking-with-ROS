#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May  1 01:09:09 2018

@author: ugot
"""
from time import time
from darkflow.net.build import TFNet
        
class objectDetector:
        def __init__(self, options):
            self.options = options
            self.tfnet = TFNet(options)
        
        def detect_object(self, image):
            start = time()
            result = self.tfnet.return_predict(image)
            #print("PREDICTION TIME", time() - start)
            return result 
