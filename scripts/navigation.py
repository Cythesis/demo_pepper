#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

# Requires robot to be in predetermined starting point.

# Script Functionalities:
# Subscribe to odometry topic of robot and print the position and z angle of robot.

import qi
import argparse
import sys
import time
import pdb
import numpy

import sys
import copy
import rospy
import moveit_commander
import moveit_msgs.msg
import geometry_msgs.msg
from nav_msgs.msg import Odometry
import math

junk_pile = [4.06,-3.3,-0.742,0.669]
original_boxes = [3.48,-3.22,-0.994,0.096]
junk_management_table = [3.76,-1.61,-0.948,0.318]
nao_robot = [9.42,4.11,0.539,0.842]
beam_robot = [11.11,2.08,-0.348,0.937]
pepper_robot = [10.95,-0.66,-0.505,0.863]
odom = [0,0,0]
flag = 0
 
def quaternionToEulerZ(x, y, z, w):
        t0 = +2.0 * (w * x + y * z)
        t1 = +1.0 - 2.0 * (x * x + y * y)
        roll_x = math.atan2(t0, t1)
     
        t2 = +2.0 * (w * y - z * x)
        t2 = +1.0 if t2 > +1.0 else t2
        t2 = -1.0 if t2 < -1.0 else t2
        pitch_y = math.asin(t2)
     
        t3 = +2.0 * (w * z + x * y)
        t4 = +1.0 - 2.0 * (y * y + z * z)
        yaw_z = math.atan2(t3, t4)
     
        return yaw_z 

# Initialize app
try:
    app = qi.Application(url='tcp://192.168.1.21:9559')
except RuntimeError:
    print ("Can't connect to Pepper")
    sys.exit(1)
ls = []
app.start()
session = app.session

def start(service, session = session):
	ls.append(service) if service not in ls else ls
	return session.service(service)

faceCharacteristic = start('ALFaceCharacteristics')
notification = start('ALNotificationManager')
autonomousLife = start('ALAutonomousLife')
callback = start('ALExpressionWatcher')
speech = start('ALSpeechRecognition')
tactile = start('ALTactileGesture')
navigation = start('ALNavigation')
posture = start('ALRobotPosture')
recharge = start('ALRecharge')
tts = start('ALTextToSpeech')
battery = start('ALBattery')
memory = start('ALMemory')
motion = start('ALMotion')
mood = start('ALMood')

def battery(tts = tts, battery = battery):
    tts.setParameter("pitchShift", 1)
    tts.setParameter('volume',20)
    tts.say('I have' + str(battery.getBatteryCharge()) + 'per cent remaining')

def moveToOdom(x,y,qz,qw):
	print("Current position is: " + str(odom[0]) + "," +str(odom[1]))
	print("Target position is: "+ str(x) + "," + str(y))
	pos_x = x-odom[0]
	pos_y = y-odom[1]
	theta = quaternionToEulerZ(0,0,qz,qw) - odom[2]
	
	motion.moveTo(0,0,-odom[2])

	answ = raw_input("Robot will navigate to " + str(round(pos_x,2)) + "," + str(round(pos_y,2)) + "," + str(round(theta,2)) + " | confirm (y/n)?")
	if (answ == "y"):
		error_code = navigation.navigateTo(pos_x,pos_y,theta)
		print(error_code)


def callback(data):
	# print("Odom data received")
	global odom
	position = data.pose.pose.position
	quart = data.pose.pose.orientation
	zAngle = quaternionToEulerZ(quart.x,quart.y,quart.z,quart.w)
	odom = [position.x, position.y, zAngle]

    
def core():
	global flag
	rospy.init_node('listener', anonymous=True)
	rospy.Subscriber("/naoqi_driver/odom", Odometry, callback)
	print("Waiting for message")
	rospy.wait_for_message("/naoqi_driver/odom", Odometry, timeout = None)
	print("Message received")
	print("Executing movements")
	moveToOdom(0,0,0,1)
	print("Movement complete")
	# while not rospy.is_shutdown():
	# 	print(odom)
	# 	rospy.sleep(1)
	# 	if (odom[0] == 0):
	# 		print("Odom is still zero")
	# 	elif (odom[0] != 0) & (flag == 0):
	# 		flag = 1
	# 		print(odom)
	# 		moveToOdom(junk_pile[0],junk_pile[1],junk_pile[2],junk_pile[3])


if __name__ == '__main__':
    try:
        core()
    except rospy.ROSInterruptException:
        pass