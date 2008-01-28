#!/usr/bin/env python

import threading, time

class TestThreadTimeout(Exception):
	pass

class TestThread(threading.Thread):
	def __init__(self,n):
		threading.Thread.__init__(self)
		self.should_stop=threading.Event()
		self.n=n
		self.exception=TestThreadTimeout
	def run(self):
		for k in xrange(self.n):
			time.sleep(0.1)
			print k
			if self.should_stop.isSet():
				break

if __name__=="__main__":
	testThread=TestThread(20)
	testThread.start()
	print "coucou"
	testThread.join(1)
	print "quitting"
	if testThread.isAlive():
		testThread.should_stop.set()
		raise TestThreadTimeout("timeout !!!")
