#!/usr/bin/env python


import sys
import qi
import argparse

import time
import pdb

class pepper():
	def __init__(self,app):
		self.session = app.session

		self.motion = self.session.service('ALMotion')

		while 1:
			position = self.motion.getAngles('RArm', False)
			position2 = self.motion.getAngles('RHand', False)
			print("")
			print("RArm")
			print(position)
			print("RHand")
			print(position2)
			time.sleep(1)

    

if __name__ == "__main__":
    try:
        app = qi.Application(url='tcp://192.168.1.2:9559')
        app.start()
    except RuntimeError:
        print ("Can't connect to Pepper")
        sys.exit(1)

    pepper = pepper(app)
    app.run()
    pepper.tts.say('Disconnecting')
    pepper.exit()


