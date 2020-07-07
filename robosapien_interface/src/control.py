#!/usr/bin/env python
import json, time

import rospy
from std_msgs.msg import String
from robomsgs.msg import RoboImageData 
import sys
from robosapien import RobosapienSlow
from scripts.ImageDetails import CameraDistance, Pixelwidth


class DecisionMaker():
    def __init__(self):
        self.subscriber = rospy.Subscriber("image_features", RoboImageData, self.process_image_output, queue_size=1, buff_size=2**24)
        #rospy.Subscriber("image_features", String, self.process_ball_detector_output)
        self.last_seen_ball_side = 'left'
        print("Done creating node")

    def process_image_output(self, data):
	RobosapienSlow.stop()
    
	rospy.loginfo("Stopping the robot for next command")
        rid = data
  	    print(rid)
	    #print("Stopping Robot for next command")
        if rid.ballFound == True and rid.ballInRange:
            if rid.postFound:
                print("Shooting the ball")
		        time.sleep(2)
            else:
                if rid.postLastFound == "left":
                    print("turning left")
                    RobosapienSlow.turn_left()
                    #time.sleep(2)
                else:
                    print("turning right")
                    RobosapienSlow.turn_right()
                    #time.sleep(2)

        elif rid.ballFound:
            print("moving to ball")
            RobosapienSlow.walk_forward()


        else:
            print("Last seen ball side fro, message:", rid.ballLastFound)
            if rid.ballLastFound == "left":
                print("turning left")
                RobosapienSlow.turn_left()
                #time.sleep(2)
            else:
                print("turning right")
                RobosapienSlow.turn_right()
                #time.sleep(2)
        
            

	                                  
    
    def move_robot_to_ball(self):
        RobosapienSlow.walk_forward()
        #time.sleep(2)

    def move_robot_to_search(self):
        if self.last_seen_ball_side == "left":
            print("turning left")
            RobosapienSlow.turn_left()
            #time.sleep(2)
        else:
            print("turning right")
            RobosapienSLow.turn_right()
            #time.sleep(2)

def main(args):
    rospy.init_node("DecisionMaker", anonymous=True)
    DM = DecisionMaker()
    try:   
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down")

if __name__ == '__main__':
    main(sys.argv)

