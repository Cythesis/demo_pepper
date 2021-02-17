#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import time
import pdb

# Initialize app
try:
    app = qi.Application()
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

def onNotification(value):
	print(notification.notifications())
# "Subscribe" to notification changes
expression_obj2 = callback.add("'NotificationAdded'",2)
signal_id2 = expression_obj2.signal.connect(onNotification)

# Breakpoint
pdb.set_trace()
