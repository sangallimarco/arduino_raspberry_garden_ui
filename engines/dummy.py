#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from generic import *

########################################
class actionTimer(genericTimer):
	def __init__(self,actions,callback):
		genericTimer.__init__(self,actions,callback)
		
	def run(self):
		print "Started"
		while len(self.actions)>0:
			pin,status,delay =self.actions.pop(0)
			print "Timer action: %s, status:%s, delay:%s" % (pin, status, delay)
			self.callback(pin,status)
			#
			time.sleep(delay)
		#release
		self.stop()
		print "Thread exit"

########################################
class customEngine(genericEngine):
	def __init__(self,host,pins):
		genericEngine.__init__(self,[int(x) for x in pins],actionTimer)
		print "Dummy Controller, Please check your config"

	def setup(self):
		for pin in self.pins:
			print "Reset pin: %s" % pin

	def createCmd(self,pin,on,off):
		print "Create command pin: %s" % pin
		return [
				[pin,1,on],
				[pin,0,off]
				]

	def sendCmd(self,pin,status):
		print "Send command: %s -> %s" % (pin,status)
