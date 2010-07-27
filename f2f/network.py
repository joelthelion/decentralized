from sys import stderr
import time
import xmpp
from daemon import storage

def start_network():
    print >>stderr, "Network started!"
    while True:
        jid=storage.config.get("jabber_id","test@example.com")
        print jid
        time.sleep(4)
