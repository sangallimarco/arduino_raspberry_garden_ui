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
		#get from postcode forecast
		url="http://www.myweather2.com/developer/forecast.ashx?uac=%s&query=%s&output=json" % (self.apikey,self.params['postcode'])
		
		#check cache
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
			current = res['weather']['curren_weather'][0]
			#no rain data grep from text
			wt = current['weather_text'].upper()
			rl = ['MIST','RAIN','DRIZZLE']
			
			#check if it's raining
			rain = False
			for i in rl:
				if i in wt:
					rain = True
					
			temp=int(current['temp'])
			humidity=int(current['humidity'])
			wind=int(current['wind'][0]['speed'])
			
			#check conditions
			if humidity<=self.params['humidity'] and wind<=self.params['wind'] and temp>=self.params['temp']:
				switch=True

		#print res
		return switch,{'temp':temp,'humidity':humidity,'wind':wind,'rain':rain,'current':wt}
			

