#!/usr/bin/env python

import json, time
import base64
import sys, time
import datetime
import numpy as np
import cv2
from robomsgs.msg import RoboImageData
from std_msgs.msg import String
from sensor_msgs.msg import Image

import roslib
import rospy
from detector import *
from central import get_ball
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError

from dynamic_reconfigure.server import Server
from image_detector.cfg import image_dectectorConfig

class ball_finder:
    def __init__(self):
        self.bridge = CvBridge()
        
        self.img_sub = rospy.Subscriber("/usb_cam_head/image_raw/compressed",
            CompressedImage,  self.callback, queue_size=1, buff_size=2**24)
        self.features_publisher = rospy.Publisher("image_features", Image, queue_size=1)
        self.redLower = (0, 120, 125)
        self.redUpper = (10, 255, 255)

        self.redLower = (170, 157, 125)
        self.redUpper = (179, 255, 255)
        self.srv = Server(image_dectectorConfig, self.dy_config_callback)

        self.rid = RoboImageData()
        self.last_ball_seen = 'left'

    def dy_config_callback(self,config, level):
        self.redLower = np.array([config.lower_red_r, config.lower_red_g,config.lower_red_b])
        self.redUpper = np.array([config.upper_red_r, config.upper_red_g,config.upper_red_b])
        return config
        
    def callback(self, data):
        print("image data got here")
        np_arr = np.fromstring(data.data, np.uint8)
        cv_image = cv2.imdecode(np_arr, 1) 
        cv2.imwrite('/home/ugot/darkflow/train/dataset_bf/img'+str(datetime.datetime.now())+'.jpg', cv_image)    
        cv2.imshow("bbox", cv_image)
        cv2.resizeWindow("Image Window",200,200)
        cv2.waitKey(3) 

        

def nothing(x):
        pass
    
def main(args):
    rospy.init_node("ball_finder", anonymous=True)
    bf = ball_finder()
    #bf.publisher()
    try:
        
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down finder")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
