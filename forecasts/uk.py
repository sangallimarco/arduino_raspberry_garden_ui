#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re,time, json
import requests
import time
import pickle
from libs.cache import memCache

########################################
class customBridge(object):
	def __init__(self,apikey='.frFFHX1sj'):
		self.params = {}
		self.cache = memCache()
		self.postcode = 'RM9'
		self.apikey = apikey
		self.file = 'app.cfg'
		#get from stored params
		self.__init()

	def __init(self):
		try:
			self.params = pickle.load(open(self.file,'r'))
		except:
			self.params = {'temp':5,'humidity':90,'wind':8,'delay':60*5,'postcode':'RM9'}

	def setParams(self,temp,humidity,wind,delay,postcode):
		self.params['temp'] = int(temp)
		self.params['humidity']= int(humidity)
		self.params['wind'] = int(wind)
		self.params['delay'] = int(delay)
		self.params['postcode'] = postcode
		#save
		pickle.dump(self.params,open(self.file,'w'))
		#remove chached value
		self.cache.unset('forecast')

	def getParams(self):
		return self.params

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
				self.cache.set('forecast',res)
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
			

