#!/usr/bin/env python
# -*- coding: utf-8 -*-


import re,time, json
import requests
import time
import pickle
from libs.cache import memCache

class genericBridge:
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

	def cacheResult(self,params):
		self.cache.set('forecast',params)

	def getForecast(self):
		#print res
		return switch,{'temp':0,'humidity':0,'wind':0,'rain':0,'current':0}
			

