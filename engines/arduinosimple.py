#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libs.ardutelnet import engineManager
from generic import *
import time

########################################
class actionTimer(genericTimer):
	def __init__(self,actions,callback):
		genericTimer.__init__(self,actions,callback)

	def run(self):
		while len(self.actions)>0:
			cmd,t=self.actions.pop(0)
			print "SENDING CMD: %s" % cmd[:-1]
			self.callback(cmd)
			#
			time.sleep(t)
		#release
		self.stop()
		
########################################
class customEngine(engineManager,genericEngine):
	def __init__(self,host, pins,bridge):
		genericEngine.__init__(self,pins,actionTimer)
		engineManager.__init__(self,host)

	#called from engineManager and genericEngine when stopped 		
	def setup(self):
		if self.isConnected():
			print "RESET SYSTEM"
			#append 
			cmd = [
				"*\n",
				"*\n",
			]
			#add pins
			for i in self.pins:
				cmd.append("#%s>1\n" % i)
			self.cmd=cmd+self.cmd

			#set thread tick
			#self.setTick(0.5)
	
	def onData(self,engine,data):
		print "DATA FROM ARDUINO: %s" % data[:-1]
		
	def createCmd(self,pin,on,off):
		cmd = [
			["#>%s1\n" % pin,on], #open valve
			["#>%s0\n" % pin,off], #close valve
		]
		return cmd

