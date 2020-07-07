# -*- coding: utf-8 -*-
"""
Created on Sun May 27 01:30:01 2018

@author: ugot
"""
import cv2
import math


class Pixelwidth:
    def __init__(self, bounding_box_coords):
        self.bounding_box_coords = bounding_box_coords
          
        
    def getWidth(self):
        bbc = self.bounding_box_coords        
        TLx = bbc['top_left'][0]
        TLy = bbc['top_left'][1]
        BRx = bbc['bottom_right'][0]
        BRy = bbc['bottom_right'][1]
        #TRx = BRx
        #TRy = TLy
        BLx = TLx
        BLy = BRy
        #calculate width
        delta_x = (BRx-BLx)**2
        delta_y = (BRy-BLy)**2
        pixel_width = math.sqrt(delta_x + delta_y)
        #calculate height
        delta_x = (BLx-TLx)**2
        delta_y = (BLy-TLy)**2
        pixel_height = math.sqrt(delta_x + delta_y)
        box_dimensions = {'BW':pixel_width, 'BH':pixel_height}                        
        return box_dimensions 


class CameraDistance:
    def __init__(self, pxWidth, knownWidth=8, focalLength=3.04):
        self.knownWidth = 8 #knownWidth
        self.focalLength = 3.04 / 10 #focalLength
        self.pxWidth = pxWidth            
    
    def distance_to_camera(self):
        #pxWidth = self.pxWidth
        #compute and return the distance from the object to the camera
        print (self.knownWidth, self.focalLength, self.pxWidth)
        return (self.knownWidth * self.focalLength * 360) / self.pxWidth

class drawBox:
    def __init__(self, image,boundingbox):
        self.image = image
        self.boundingbox = boundingbox        

    def bounding_box(self):            
        bbc = self.boundingbox
        topleft = bbc['TL'] 
        bottomright = bbc['BR']        
        image = cv2.rectangle(self.image,topleft, bottomright, 255, 2)
        return image
