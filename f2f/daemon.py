# the main daemon, handling the data store and rating posts
from Queue import Queue
from sys import stderr

post_queue=Queue()

def start_daemon():
    import time
    while True:
        if not post_queue.empty():
            print >>stderr, post_queue.get()
        else:
            print >>stderr, "empty!"
        time.sleep(1)
