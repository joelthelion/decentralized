from sys import stderr
import time
import xmpp


def start_network():
    print >>stderr, "Network started!"
    while True:
        time.sleep(1)
