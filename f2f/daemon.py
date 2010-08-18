# the main daemon, handling the data store and rating posts
from Queue import Queue
from sys import stderr
from persistence import PersistentObject,basedir

post_queue=Queue()

class StorageObject(PersistentObject):
     storage_file=basedir+"daemon.pck"
     def __init__(self):
        PersistentObject.__init__(self)
        if not self.__dict__.has_key("my_posts"):
            self.my_posts=[]
        if not self.__dict__.has_key("config"):
            self.config={}

storage=StorageObject()

def add_post():
    from network import outbox
    print >>stderr, "New post taken into account."
    new_post=post_queue.get()
    outbox.put(new_post) # send the new post over the network
    storage.my_posts.append(new_post)
    storage.store() #we don't want to lose posts

def start_daemon():
    from network import outbox
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
