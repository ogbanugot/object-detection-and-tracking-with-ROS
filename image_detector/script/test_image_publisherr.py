#!/usr/bin/env python

import rospy
import cv2
import glob
from sensor_msgs.msg import Image, CompressedImage
from cv_bridge import CvBridge, CvBridgeError

images = [cv2.imread(file) for file in glob.glob('/home/ugot/Atest_images/post/*jpg')]
print("Number of images found: " + str(len(images)))

rospy.init_node("robo_data_publiaher", anonymous=True)
image_publisher = rospy.Publisher("/raspicam_node/image/compressed", Image, queue_size=1)

rate = rospy.Rate(0.1)
index = 0
while not rospy.is_shutdown():

    np_img = images[index % len(images)]
    print(np_img.shape)
    msg_frame = CvBridge().cv2_to_imgmsg(np_img, "bgr8")
    image_publisher.publish(msg_frame)
    print("Publishing image features")
    rate.sleep()
    index += 1
