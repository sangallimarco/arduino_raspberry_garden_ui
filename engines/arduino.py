#!/usr/bin/env python
# -*- coding: utf-8 -*-
from libs.ardutelnet import engineManager
from generic import *
import time

########################################
class actionTimer(genericTimer):
	def __init__(self,actions,callback):
		genericTimer.__init__(self)
		self.actions=actions
		self.callback=callback
		self.start()

	def run(self):
		while len(self.actions)>0:
			cmd,t=self.actions.pop(0)
			print "SENDING CMD: %s" % cmd[:-1]
			self.callback(cmd)
			#
			time.sleep(t)
		#release
		self.callback = None
		
########################################
class customEngine(engineManager,genericEngine):
	def __init__(self,host, pins,bridge):
		genericEngine.__init__(self,actionTimer)
		self.bridge = bridge
		self.pins = pins
		self.timer = None

		engineManager.__init__(self,host)
		
	def onConnect(self):
			print "RESET SYSTEM"
			#append 
			cmd = [
				"*\n",
				"*\n",
				"#>%s1\n" % self.bridge #reset bridge
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
			["#>%s0\n#>%s0\n" % (self.bridge,pin), off], #open valve
			["#>%s0\n#>%s1\n" % (self.bridge,pin), off], #change bridge
			["#>%s1\n#>%s1\n" % (self.bridge,pin), on], #sleep
			["#>%s1\n#>%s0\n" % (self.bridge,pin), off], #close valve
			["#>%s1\n#>%s1\n" % (self.bridge,pin), off] #sleep
		]
		return cmd

########################################
if __name__=="__main__":
	e=customEngine("192.168.1.177",["D","E","F","G"])
	#send command
	while 1:
		if e.isConnected():
			#pumps on!
			e.pumpsOn(10)
			#
			time.sleep(120)
		else:
			time.sleep(2)
		
		print "----------------"
