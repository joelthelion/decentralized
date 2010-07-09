#!/usr/bin/env python

#Main program to start the different threads


if __name__=='__main__':
    import thread
    from webserver import start_server
    import time
    thread.start_new_thread(start_server,())
    while True:
        time.sleep(1)
