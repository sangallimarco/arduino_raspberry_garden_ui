#import pickle
import time

#volatile memory cache
class memCache(object):
	def __init__(self):
		self.cache = {}

	def set(self,key,val,ttl=30):
		self.cache[key] = (time.time()+ttl, val)

	def get(self,key):
		try:
			ttl,val = self.cache[key]
		except:
			return None
		else:
			#check ttl
			if time.time()<=ttl:
				return val
			else:
				return None

	def unset(self,key):
		try:
			del self.cache[key]
		except:
			pass

#tests
if __name__=="__main__":
	c = memCache()
	print c.get('test')
	
	c.set('test','ok',3)
	c.unset('test')
	print c.get('test')

	c.set('test','ok',3)
	time.sleep(1)
	print c.get('test')
	
	time.sleep(4)
	print c.get('test')