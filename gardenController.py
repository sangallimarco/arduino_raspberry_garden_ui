# -*- coding: utf-8 -*-
from libs.ardutelnet import engineManager
from threading import Thread
import urllib2,re,time, json
import requests
import time
import pickle
from libs.cache import memCache

########################################
class gardenBridge(object):
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
			
########################################
class actionTimer(Thread):
	def __init__(self,actions,callback):
		Thread.__init__(self)
		self.actions=actions
		self.callback=callback
		self.start()

	def isAlive(self):
		return True
		
	def run(self):
		while len(self.actions)>0:
			cmd,t=self.actions.pop(0)
			print "SENDING CMD: %s" % cmd[:-1]
			self.callback(cmd)
			#
			time.sleep(t)
			
########################################
class pinger(Thread):
	def __init__(self,callback):
		Thread.__init__(self)
		self.callback=callback
		self.start()
		
	def run(self):
		while 1:
			print "SENDING PING"
			self.callback("#~A0\n")
			#
			time.sleep(1)
		
########################################
class customEngine(engineManager):
	def __init__(self,host):
		#@@@p=pinger(self.sendCmd)
		self.bridge = "C"
		self.pins = ["D","E","F","G"]
		self.time = None

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
		
	def pumpsOn(self,on=10,off=1):
		#pass all to a timer
		cmd = []
		for i in self.pins:
			cmd += self.createCmd(i,on,off)
		#
		self.timer=actionTimer(cmd,self.sendCmd)
		
	def singlepumpOn(self,on=10,off=2):
		#pass all to a timer
		cmd = self.createCmd(self.pins[0],on,off)
		#
		self.timer=actionTimer(cmd,self.sendCmd)

	def isReady(self):
		try:
			self.timer.isAlive()
		except:
			return False
		else:
			return True

########################################
if __name__=="__main__":
	e=customEngine("192.168.1.177")
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

