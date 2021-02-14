#! /usr/bin/env python
# -*- encoding: UTF-8 -*-

import qi
import argparse
import sys
import time
import pdb
import scipy.misc
import numpy

# '/home/nao/.local/share/Explorer/2021-01-13T061256.268Z.explo' r5 path
# '/home/nao/.local/share/Explorer/2021-01-14T012852.035Z.explo' r5 base path

class Localization:
	def explore(self, radius):
		return navigation.explore(radius)

	def saveMap(self):
		return navigation.saveExploration()

	def saveMapToImage(self, name):
		result_map = navigation.getMetricalMap()
		map_width = result_map[1]
		map_height = result_map[2]
		img = numpy.array(result_map[4]).reshape(map_width, map_height)
		img = (100 - img) * 2.55 
		img = numpy.array(img, numpy.uint8)
		scipy.misc.imsave(name, img)

	def stop(self):
		navigation.stopExploration()

	def loadAndLocalize(self,path,guess):
		navigation.loadExploration(path)
		navigation.relocalizeInMap(guess)
		navigation.startLocalization()


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

lmap = Localization()
expression_obj2 = callback.add("'NotificationAdded'",2)
signal_id2 = expression_obj2.signal.connect(onNotification)


# Functions to make things easier

# Breakpoint
pdb.set_trace()