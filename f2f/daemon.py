# the main daemon, handling the data store and rating posts
from Queue import Queue
from sys import stderr
import persistence

post_queue=Queue()
my_posts=[]

persistence_dict={"my_posts" : my_posts}
persistence_doer=persistence.do_persistence(persistence_dict)

def add_post():
    new_post=post_queue.get()
    my_posts.append(new_post)

def start_daemon():
    import time
    while True:
        if not post_queue.empty():
	    add_post()
            #print >>stderr, post_queue.get()
        else:
            pass#print >>stderr, "empty!"
	persistence_doer.next()
        time.sleep(1)
