from sys import stderr
import time
import xmpp
from daemon import storage

def connect(jid,password):
    jid=xmpp.protocol.JID(jid)
    cl=xmpp.Client(jid.getDomain(),debug=[])
    con=cl.connect()
    if not con:
        print >>stderr, 'could not connect!'
    auth=cl.auth(jid.getNode(),password,resource=jid.getResource())
    print >>stderr, con
    print >>stderr, auth
    if not auth:
        print >>stderr, 'could not authenticate!'
    return cl

def message_handler(client,message):
    print >>stderr, message

def start_network():
    jid=storage.config.get("jabber_id","test@example.com")
    password=storage.config.get("jabber_password","xxx")
    print >>stderr, jid,password
    client=connect(jid,password)
    client.sendInitPresence()
    client.RegisterHandler('message',message_handler)
    print >>stderr, "Network started!"
    while True:
        #print jid
        client.Process(1)
        time.sleep(1)
