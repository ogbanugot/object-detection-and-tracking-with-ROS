#!/usr/bin/env python

import json
import base64
import sys, time
import datetime
import numpy as np
import cv2
from std_msgs.msg import String
import math 
import roslib
import rospy
from detector import *
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError
from object_detector import objectDetector
import imutils
from robosrvs.srv import *

ball_options = { 
            "pbLoad": "/home/ugot/darkflow/built_graph/yolov2-tiny-1c.pb", 
            "metaLoad": "/home/ugot/darkflow/built_graph/yolov2-tiny-1c.meta", 
            "threshold": 0.3,
            }

post_options = { 
            "pbLoad": "/home/ugot/darkflow/built_graph/yolov2-tiny-2c.pb", 
            "metaLoad": "/home/ugot/darkflow/built_graph/yolov2-tiny-2c.meta", 
            "threshold": 0.3,
            }


class ball_finder:
    def __init__(self):
        
        self.bridge = CvBridge()
        self.rid = RoboImageData()
        self.last_ball_seen = 'left'
        self.last_post_seen = 'left'
        # self.ball_bounding_box = {}
        # self.post_bounding_box = {}
        self.ballcallback_image = None
        self.postcallback_image = None
        self.away_post = "violetpost"
        self.ball_detector = objectDetector(ball_options)
        self.post_detector = objectDetector(post_options)
        self.ball_img_sub = rospy.Subscriber("/usb_cam_head/image_raw/compressed", CompressedImage, self.ball_callback, queue_size = 1, buff_size=2**24)
        self.post_img_sub = rospy.Subscriber("/raspicam_node/image/compressed", CompressedImage, self.post_callback, queue_size = 1, buff_size=2**24)


    def ball_callback(self, data):
        rospy.loginfo("Ball callback data got here")
        np_arr = np.fromstring(data.data, np.uint8)
        cv_image = cv2.imdecode(np_arr, 1)          
        self.ballcallback_image = imutils.resize(cv_image,width=300)

    def check_ball_side(self, bounding_box_coord, image_center, post_ball):
        top_left = bounding_box_coord.get("top_left")
        bottom_right = bounding_box_coord.get("bottom_right")
        mid_x = (top_left[0] + bottom_right[0])/2
        #print("Mid X found: ", mid_x)
        if post_ball == "ball":
            if mid_x < image_center[0]:
                self.last_ball_seen = "left"
            elif mid_x > image_center[0]:
                self.last_ball_seen = "right"
            # print("Side Ball Image Found: ", self.last_ball_seen)
        elif post_ball == "post":
            if mid_x < image_center[0]:
                self.last_post_seen = "left"
            elif mid_x > image_center[0]:
                self.last_post_seen = "right"
            # print("Side Post Image Found: ", self.last_post_seen)
    
    def post_callback(self, data):
        rospy.loginfo("Post callback data got here")
        np_arr = np.fromstring(data.data, np.uint8)
        cv_image = cv2.imdecode(np_arr, 1)            
        self.postcallback_image = imutils.resize(cv_image,width=300)        


    def ballDetector(self, ball_image):
        cv_image_resize = ball_image
        result = self.ball_detector.detect_object(cv_image_resize) 
        ball_bounding_box = {}
        if len(result) > 0:
            for object_detected in result:
                if object_detected.get("label") == "ball" and object_detected.get("confidence")>0.2:                       
                    confidence = object_detected.get("confidence")
                    #print(confidence)
                    ball_label = object_detected.get("label")
                    top_left = object_detected.get("topleft")
                    bottom_right = object_detected.get("bottomright")

                    ball_bounding_box = {
                                    "top_left" : (top_left.get("x"), top_left.get("y")),
                                    "bottom_right" : (bottom_right.get("x"), bottom_right.get("y")),
                    }
                    
        #print(self.ball_bounding_box)                   
        cv_image_resize = draw_bounding_box(cv_image_resize,ball_bounding_box,(255,255,0),thickness=3)                      
        cv2.imshow("bbox2", cv_image_resize)
        cv2.resizeWindow("Image Window",200,200)
        cv2.waitKey(3)
        return ball_bounding_box 

    def postDetector(self, post_image):
        cv_image_resize = post_image
        result = self.post_detector.detect_object(cv_image_resize) 
        post_bounding_box = {} 
        if len(result) > 0:
            for object_detected in result:
                if object_detected.get("label") == self.away_post and object_detected.get("confidence")>0.2:
                        confidence = object_detected.get("confidence")
                        #print(confidence)
                        ball_label = object_detected.get("label")
                        print(ball_label)
                        top_left = object_detected.get("topleft")
                        bottom_right = object_detected.get("bottomright")

                        post_bounding_box = {
                                    "top_left" : (top_left.get("x"), top_left.get("y")),
                                    "bottom_right" : (bottom_right.get("x"), bottom_right.get("y")),
                        }
        # print(self.post_bounding_box)      
        # cv_image_resize = draw_bounding_box(cv_image_resize,post_bounding_box,(255,232,77),thickness=3)   
        # cv2.imshow("bbox1", cv_image_resize)
        # cv2.resizeWindow("Image Window",200,200)
        # cv2.waitKey(3)
        return post_bounding_box



    def publisher(self):
        # 0.5 = 2sec
        # 0.2 = 5sec
        # 0.1 = 10sec
        # rate = rospy.Rate(2)
        rospy.Rate(0.5).sleep()
        iterations = 0
        while not rospy.is_shutdown(): 
            print("######################################################################### " + str(iterations)) 
            rospy.wait_for_service('move_robot')
            try:
                while self.ballcallback_image is not None:
                    move_robot = rospy.ServiceProxy('move_robot', RoboImageSrvData)
                    rospy.loginfo("Predicting...")
                    ball_bounding_box = self.ballDetector(self.ballcallback_image)
                    post_bounding_box = self.postDetector(self.postcallback_image)
                    ballFound = bool(ball_bounding_box)
                    postFound = True #bool(post_bounding_box)
                    rospy.loginfo("Done Predicting.")
                    ballLastFound = self.last_ball_seen
                    ballInRange = False
                    postLastFound = self.last_post_seen

                    if False:
                        self.check_ball_side(post_bounding_box,(255,300), "post")
                        postLastFound = self.last_post_seen

                    if ballFound:
                        self.check_ball_side(ball_bounding_box,(255,300), "ball")
                        ballLastFound = self.last_ball_seen
                        if (ball_bounding_box['bottom_right'][1]>200 and ball_bounding_box['top_left'][1]>60):
                            ballInRange = True
                        else:
                            ballInRange = False
                    else:
                        ballInRange = False

                    rospy.loginfo("Sending image features to server")
                    print("ballLastFound: ",ballLastFound, "ballFound", ballFound, "ballInRange", ballInRange, "postFound", postFound, "postLastFound", postLastFound)
                    resp1 = move_robot(ballLastFound, ballFound, ballInRange, postFound, postLastFound, iterations)
                    rospy.loginfo("Server Resp: " + str(resp1.done))
                    iterations += 1
                    self.ballcallback_image = None
                    #self.postcallback_image = None
            except rospy.ServiceException, e:
                print "Service call failed: %s"%e



def getArea(bounding_box_coords):
    bbc = bounding_box_coords     
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
    area = pixel_width * pixel_height    
    return area 


def nothing(x):
        pass
    
def main(args):
    rospy.init_node("move_robot_client", anonymous=True)
    bf = ball_finder()
    bf.publisher()
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down finder")

if __name__ == '__main__':
    main(sys.argv)
