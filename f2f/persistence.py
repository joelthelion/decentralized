import cPickle as pickle
import os

storage_file="~/.config/f2f.pck"

def do_persistence(persistence_dict):
    import time
    t=0
    while True:
        if time.time() - t > 120: #save every two minutes
	    with open(os.path.expanduser(storage_file),"w") as file:
                t=time.time()
                pickle.dump(persistence_dict,file)
                yield None

def restore_dict()
    with open(os.path.expanduser(storage_file),"w") as file:
        return pickle.load(file)
