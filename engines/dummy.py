#!/usr/bin/env python
# -*- coding: utf-8 -*-

from threading import Thread
import time

########################################
class actionTimer(Thread):
	def __init__(self,actions,callback):
		Thread.__init__(self)
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
class customEngine(object):
	def __init__(self,host,pins,bridge):
		print "Dummy Controller, Please check your config"

	def isConnected(self):
		return True

	def createCmd(self,pin,on,off):
		print "Create command"

	def sendCmd(self):
		print "Send command"

	def pumpsOn(self,on=10,off=1):
		print "All Pumps On"
		self.timer=actionTimer([1,2,3,4],self.sendCmd)

	def singlepumpOn(self,on=10,off=2):
		print "Simgle Pump On"
		self.timer=actionTimer([1,2,3,4],self.sendCmd)

	def isReady(self):
		try:
			status = self.timer.isAlive()
		except:
			return True
		else:
			return not status
		
