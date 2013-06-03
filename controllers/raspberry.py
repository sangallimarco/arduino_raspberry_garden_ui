#http://code.google.com/p/raspberry-gpio-python/wiki/Outputs
#http://elinux.org/RPi_Low-level_peripherals#GPIO_hardware_hacking

from threading import Thread
import RPi.GPIO as GPIO

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
			pin,status,t=self.actions.pop(0)
			print "GPIO CMD: %s>%d" % (pin,status)
			self.callback(pin,status)
			#
			time.sleep(t)

########################################
class customEngine(object):
	def __init__(self,host,pins,bridge):
		#convert to int
		self.bridge = int(bridge)
		self.pins = [int(x) for x in pins]
		self.timer = None
		#set board mode
		GPIO.setmode(GPIO.BOARD)
		#init pins
		for i in self.pins:
			GPIO.setup(i, GPIO.OUT)

	def isConnected(self):
		return True

	def createCmd(self,pin,on,off):
		cmd = [
			[pin, 1, on], #open valve
			[pin, 0, off] #close
		]
		return cmd

	def sendCmd(self,pin,status):
		GPIO.output(pin,status)

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
			return True
		else:
			return False

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