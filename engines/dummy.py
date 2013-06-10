#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time
from generic import *

########################################
class actionTimer(genericTimer):
	def __init__(self,actions,callback):
		genericTimer.__init__(self)
		self.actions=actions
		self.callback=callback
		self.alive=True
		self.start()
		
	def run(self):
		print "Started"
		while len(self.actions)>0:
			action=self.actions.pop(0)
			print action
			self.callback()
			#
			time.sleep(5)
		#release
		self.callback = None

########################################
class customEngine(genericEngine):
	def __init__(self,host,pins,bridge):
		genericEngine.__init__(self,actionTimer)
		self.bridge = int(bridge)
		self.pins = [int(x) for x in pins]
		print "Dummy Controller, Please check your config"

	def createCmd(self,pin,on,off):
		print "Create command %s" % pin
		return [pin]

	def sendCmd(self):
		print "Send command"


