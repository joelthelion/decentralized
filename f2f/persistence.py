import cPickle as pickle
import os
from sys import stderr

storage_file="~/.config/f2f.pck"

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
