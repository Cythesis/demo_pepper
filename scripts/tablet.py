#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

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
tablet = start('ALTabletService')
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

def main():
  tablet.showInputDialog("text","Malfunction","Shutdown","Reset","Hardware is in critical condition",2)
  tablet.showImageNoCache("https://s29843.pcdn.co/blog/wp-content/uploads/sites/2/2020/11/TechSmith-Blog-JPGvsPNG-768x576.png")

if __name__=='__main__':
	try:
		main()
	except rospy.ROSInterruptException:
		pass


# Say hello

# Execute arm movements (wave + return to original pos)

# Say How u doin?
