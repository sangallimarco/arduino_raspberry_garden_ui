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
			action,delay =self.actions.pop(0)
			print "Timer action: %s, delay:%s" % (action, delay)
			self.callback()
			#
			time.sleep(delay)
		#release
		self.stop()
		print "Thread exit"

########################################
class customEngine(genericEngine):
	def __init__(self,host,pins,bridge):
		genericEngine.__init__(self,[int(x) for x in pins],int(bridge),actionTimer)
		print "Dummy Controller, Please check your config"

	def createCmd(self,pin,on,off):
		print "Create command pin: %s" % pin
		return [
				[pin,on],
				[pin,off]
				]

	def sendCmd(self):
		print "Send command"
