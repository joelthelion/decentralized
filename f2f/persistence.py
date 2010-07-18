import cPickle as pickle
import os
from sys import stderr
import time


def persistence(persistence_dict):
    import time
    t=0
    while True:
        if time.time() - t > 10: #save every two minutes
	    with open(os.path.expanduser(storage_file),"w") as myfile:
                t=time.time()
                pickle.dump(persistence_dict,myfile)
		print >>stderr, "Wrote %d links to the disk" % len(persistence_dict["my_posts"])
                yield None
        else: yield None

def restore():
    try:
        with open(os.path.expanduser(storage_file),"r") as myfile:
            return pickle.load(myfile)
    except IOError as e:
	print >>stderr, e,type(e)
        return {}

class PersistentObject:
    storage_file="~/.config/f2f.pck"
    def __init__(self):
	print >>stderr,"toto"
	if self.restore():
	    self.could_restore=True
	else:
	    self.could_restore=False
            self.last_storage_time=0
	    self.storage_interval=10
    def store(self):
        with open(os.path.expanduser(self.storage_file),"w") as myfile:
            self.last_storage_time=time.time()
            pickle.dump(self,myfile)
    def lazy_store(self):
	if time.time() - self.last_storage_time > self.storage_interval:
	    self.store()
    def restore(self):
	try:
            with open(os.path.expanduser(self.storage_file),"r") as myfile:
                self.__dict__=pickle.load(myfile).__dict__
	    	return True
        except IOError as e:
	        print >>stderr,e
		return False
    
        





