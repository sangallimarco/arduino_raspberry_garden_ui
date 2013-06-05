#!/usr/bin/env python
# -*- coding: utf-8 -*-


########################################
class customEngine(object):
	def __init__(self,host,pins,bridge):
		print "Dummy Controller, Please check your config"

	def isConnected(self):
		return True

	def createCmd(self,pin,on,off):
		print "Create command"

	def sendCmd(self,pin,status):
		print "Send command"

	def pumpsOn(self,on=10,off=1):
		print "All Pumps On"

	def singlepumpOn(self,on=10,off=2):
		print "Simgle Pump On"

	def isReady(self):
		return True
		
