#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re,time
import requests
from generic import *

########################################
class customBridge(genericBridge):
	def __init__(self):
		genericBridge.__init__(self)

	def getForecast(self):
		#
		re_red=re.compile('DB0000">([\-0-9\.]+)')
		re_green=re.compile('429108">([0-9\.]+)')
		re_purple=re.compile('C000DB">([0-9\.]+)')
		#get from postcode forecast
		url="http://www.centrometeolombardo.com/Moduli/stazioni.php?erbacentro"
		
		#check cache
		res = self.cache.get('forecast')
		if not res:
			print url
			try:
				res = requests.get(url).text
			except:
				res = False
			else:
				self.cacheResult(res)
		#
		current = ""
		temp = 0
		humidity = 0
		wind = 0
		rain = False
		switch = False

		if(res):
			red=re_red.findall(res)
			green=re_green.findall(res)
			purple=re_purple.findall(res)

			#debug
			print red,green,purple

			#remap
			temp = int(float(red[0]))
			humidity = int(float(red[1]))
			wind = int(float(green[0]))
			rain = int(float(red[4]))
			current = "CONNECTED"

			#switch or not
			if humidity<=self.params['humidity'] and wind<=self.params['wind'] and temp>=self.params['temp']:
				switch=True

		#print res
		return switch,{'temp':temp,'humidity':humidity,'wind':wind,'rain':rain,'current':current}
			

