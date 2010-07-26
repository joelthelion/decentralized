from sys import stderr
import time
import xmpp
from persistence import PersistentObject,basedir

class NetworkSettings(PersistentObject):
    storage_file=basedir+"network.pck"
     def __init__(self):
        PersistentObject.__init__(self)
        if not self.could_restore:
            self.jid=""
            self.password=""

def start_network():
    print >>stderr, "Network started!"
    while True:
        time.sleep(1)
