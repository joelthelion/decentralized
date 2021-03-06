#!/usr/bin/env python

#Main program to start the different threads


if __name__=='__main__':
    import thread
    from webserver import start_server
    from daemon import start_daemon
    from network import start_network
    import time
    thread.start_new_thread(start_server,())
    thread.start_new_thread(start_daemon,())
    thread.start_new_thread(start_network,())
    while True:
        time.sleep(1)
