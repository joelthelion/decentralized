import cPickle as pickle
import os
from sys import stderr
import time

basedir=os.path.expanduser("~/.config/f2f/")

class PersistentObject:
    storage_file=basedir + "f2f.pck"
    def __init__(self):
        if self.restore():
            self.could_restore=True
        else:
            if not os.path.exists(basedir):
                os.mkdir(basedir)
            self.could_restore=False
            self.last_storage_time=0
            self.storage_interval=10
    def store(self):
        with open(self.storage_file,"w") as myfile:
            self.last_storage_time=time.time()
            pickle.dump(self,myfile)
    def lazy_store(self):
	if time.time() - self.last_storage_time > self.storage_interval:
	    self.store()
    def restore(self):
	try:
            with open(self.storage_file,"r") as myfile:
                self.__dict__=pickle.load(myfile).__dict__
	    	return True
        except IOError as e:
	        print >>stderr,e
		return False
    
        





