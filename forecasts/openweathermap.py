#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re,time
import requests
from generic import *

# http://openweathermap.org/
########################################
class customBridge(genericBridge):
	def __init__(self):
		genericBridge.__init__(self)

	def getForecast(self):
		#get from postcode forecast
		url="http://api.openweathermap.org/data/2.5/weather?APPID=%s&q=%s" % (self.apikey, self.params['postcode'])

		#check cache
		res = False
		res = self.cache.get('forecast')
		if not res:
			print url
			try:
				res = requests.get(url).json()
			except:
				res = False
			else:
				self.cacheResult(res)
		#
		current = None
		temp = 0
		humidity = 0
		wind = 0
		rain = False
		switch = False
		wt = False

		if(res):
			#	print res
			current = res['main']

			#check if it's raining
			rain = False
			if res.has_key('rain'):
				rain = True

			wind = 0
			if res.has_key('wind'):
				wind=int(res['wind']['speed'])

			# kelvin temp
			temp=int(current['temp'] - 273.15)
			humidity=int(current['humidity'])

			#check conditions
			if humidity<=self.params['humidity'] and wind<=self.params['wind'] and temp>=self.params['temp']:
				switch=True

		#print res
		return switch,{'temp':temp,'humidity':humidity,'wind':wind,'rain':rain,'current':wt}


if __name__ == '__main__':
	a = customBridge()
	a.setParams(20,80,10,1000,'Erba, it')
	print a.getForecast()
