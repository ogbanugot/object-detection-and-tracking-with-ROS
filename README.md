<h3 align="left">Object detection and tracking using ROS, YOLOv2 and Robosapien 👋</h3>
<p>
  <img alt="Version" src="https://img.shields.io/badge/version-0.0.1-blue.svg?cacheSeconds=2592000" />
</p>

![alt text](https://github.com/ogbanugot/Obstacle-detection-and-tracking-with-ROS/blob/master/image_detector/cfg/sample.gif)

Object detection using YOLOv2 on a Robosapien robot with raspberry pi3.  
Project was exectuted for the ICogs Labs robosoccer competition in Ethiopia.

## Requirements
ROS Kinetic
YOLOv2

## Usage
First, copy the files in the repo to your catkin_ws and cmake.  
Run the object detection and tracking module.  
```sh
rosrun image_detector move_robot_client.py
```
Run the robot control module
```sh
rosrun robosapien_interface control.py
```
See this document for how to rig up your own robosapien  
https://docs.google.com/document/d/1MmpT99e-2ObdFXaL_qDeM5hU9l2JLdZPhqlyOZkqSXc/edit?usp=sharing
