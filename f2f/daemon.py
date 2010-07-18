# the main daemon, handling the data store and rating posts
from Queue import Queue
from sys import stderr
from persistence import PersistentObject

post_queue=Queue()

class StorageObject(PersistentObject):
     def __init__(self):
	  PersistentObject.__init__(self)
	  if not self.could_restore:
	      print >>stderr,"toto2"
              self.my_posts=[]

storage=StorageObject()

def add_post():
    print >>stderr, "New post taken into account."
    new_post=post_queue.get()
    storage.my_posts.append(new_post)

def start_daemon():

    import time
    while True:
	#print >>stderr, storage.my_posts
        if not post_queue.empty():
	    add_post()
            #print >>stderr, post_queue.get()
        else:
            pass#print >>stderr, "empty!"
	storage.lazy_store()
        time.sleep(1)
