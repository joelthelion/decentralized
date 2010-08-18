from Queue import Queue
from sys import stderr
import time
import xmpp

outbox=Queue()

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

def presence_handler(client,message):
    print str(message)
    prs_type=message.getType()
    sender=message.getFrom()
    if prs_type == "subscribe": #accept all friend requests
        client.send(xmpp.Presence(to=sender, typ = 'subscribed'))
        client.send(xmpp.Presence(to=sender, typ = 'subscribe'))

def start_network():
    from daemon import storage
    jid=storage.config.get("jabber_id","test@example.com")
    password=storage.config.get("jabber_password","xxx")
    #print >>stderr, jid,password
    client=connect(jid,password)
    client.sendInitPresence()
    client.RegisterHandler('presence',presence_handler)
    client.RegisterHandler('message',message_handler)
    roster=client.getRoster()
    print >>stderr, "Network started!"
    while True:
        while not outbox.empty(): #send posts to friends
            new_post=outbox.get()
            for jid in roster.getItems():
                m=xmpp.Message(to=jid,body=new_post.url,typ="message",attrs={})
                client.send(m)
        #print jid
        client.Process(1)
        time.sleep(1)
