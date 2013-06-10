#!/usr/bin/env python
# -*- coding: utf-8 -*-

#http://code.google.com/p/raspberry-gpio-python/wiki/Outputs
#http://elinux.org/RPi_Low-level_peripherals#GPIO_hardware_hacking
import RPi.GPIO as GPIO
import time
from generic import *

########################################
class actionTimer(genericTimer):
	def __init__(self,actions,callback):
		genericTimer.__init__(self)
		self.actions=actions
		self.callback=callback
		self.start()

	def run(self):
		while len(self.actions)>0:
			pin,status,t=self.actions.pop(0)
			print "GPIO CMD: %s>%d" % (pin,status)
			self.callback(pin,status)
			#
			time.sleep(t)
		#release
		self.callback = None 

########################################
class customEngine(genericEngine):
	def __init__(self,host,pins,bridge):
		genericEngine.__init__(self,actionTimer)
		#convert to int
		self.bridge = int(bridge)
		self.pins = [int(x) for x in pins]
		self.timer = None
		#set board mode
		GPIO.setmode(GPIO.BOARD)
		#init pins
		for i in self.pins:
			GPIO.setup(i, GPIO.OUT)

	def createCmd(self,pin,on,off):
		cmd = [
			[pin, 1, on], #open valve
			[pin, 0, off] #close
		]
		return cmd

	def sendCmd(self,pin,status):
		GPIO.output(pin,status)


########################################
if __name__=="__main__":
	e=customEngine([12,16,18])
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