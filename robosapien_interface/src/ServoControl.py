#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 12 00:38:53 2018

@author: ugot
"""

import RPi.GPIO as GPIO
import time

def controlServo(move, servo=22):    
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(servo,GPIO.OUT)
    p=GPIO.PWM(servo,50)# 50hz frequency
    p.start(2.5)
    if move == 'left':
        p.ChangeDutyCycle(12)
	time.sleep(0.03)
    else:
        p.ChangeDutyCycle(2)
        time.sleep(0.03)
    GPIO.cleanup()
    return move
