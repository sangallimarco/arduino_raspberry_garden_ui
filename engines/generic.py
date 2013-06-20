#!/usr/bin/env python
# -*- coding: utf-8 -*-
from threading import Thread

########################################
class genericTimer(Thread):
	def __init__(self,actions,callback):
		Thread.__init__(self)
		self.actions=actions
		self.callback=callback
		self.start()

	#empty actions
	def stop(self):
		self.actions = []
		self.callback = None

	def run(self):
		self.stop()

########################################
class genericEngine(object):
	def __init__(self,pins,timerClass = genericTimer,setup = True):
		self.pins = pins
		self.timer = None
		self.timerClass = timerClass
		#setup
		if setup:
			self.setup()

	#create your own methods
	def setup(self):
		pass

	def isConnected(self):
		return True

	def createCmd(self,pins,on,off):
		return [pins]

	def sendCmd(self):
		pass
	
	#check timer status
	def isReady(self):
		try:
			status = self.timer.isAlive()
		except:
			return True
		else:
			return not status	

	#stop timer
	def stop(self):
		try:
			self.timer.stop()
		except:
			pass
		#reinit system
		self.setup()

	#loop all the pins
	def pumpsOn(self,on=10,off=1):
		#pass all to a timer
		cmd = []
		for i in self.pins:
			cmd += self.createCmd(i,on,off)
		#
		self.timer=self.timerClass(cmd,self.sendCmd)

	#only starts the first pin
	def singlepumpOn(self,on=10,off=1):
		#pass all to a timer
		cmd = self.createCmd(self.pins[0],on,off)
		#
		self.timer=self.timerClass(cmd,self.sendCmd)

