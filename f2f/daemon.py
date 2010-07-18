# the main daemon, handling the data store and rating posts
from Queue import Queue
from sys import stderr
import persistence

post_queue=Queue()
my_posts=[]
print >>stderr,"hello!!!"


def add_post():
    print >>stderr, "New post taken into account."
    new_post=post_queue.get()
    my_posts.append(new_post)

def start_daemon():
    persistence_dict=persistence.restore()
    if persistence_dict:
        my_posts.extend(persistence_dict["my_posts"])
	persistence_dict["my_posts"] = my_posts
    else:
        print >>stderr, "No persistence file found, starting with empty containers"
        persistence_dict={"my_posts" : my_posts}
    persistence_doer=persistence.persistence(persistence_dict)

    import time
    while True:
	print >>stderr, my_posts
        if not post_queue.empty():
	    add_post()
            #print >>stderr, post_queue.get()
        else:
            pass#print >>stderr, "empty!"
	persistence_doer.next()
        time.sleep(1)
