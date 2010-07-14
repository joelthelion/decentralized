# the main daemon, handling the data store and rating posts
from Queue import Queue
from sys import stderr

post_queue=Queue()
my_posts=[]

def add_post():
    new_post=post_queue.get()
    my_posts.append(new_post)

def start_daemon():
    import time
    while True:
        if not post_queue.empty():
            print >>stderr, post_queue.get()
        else:
            pass#print >>stderr, "empty!"
        time.sleep(1)
