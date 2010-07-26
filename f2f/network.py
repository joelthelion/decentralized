from sys import stderr
import time
import xmpp
from daemon import storage

def start_network():
    print >>stderr, "Network started!"
    jid=storage.config.get("jabber_id","test@example.com")
    while True:
        print jid
        time.sleep(1)
