#!/usr/bin/env python
from daemon import storage
from network import connect,message_handler,presence_handler
import xmpp


jid=storage.config.get("jabber_id","test@example.com")
password=storage.config.get("jabber_password","xxx")
client=connect(jid,password)
client.sendInitPresence()
client.RegisterHandler('presence',presence_handler)
client.RegisterHandler('message',message_handler)
client.RegisterDefaultHandler(message_handler)
roster=client.getRoster()

f2fnode=xmpp.protocol.Node(tag="f2f",attrs={"url":"http://lemonde.fr","body":"a nice website"})
message=xmpp.Message(to="f2f_echo_bot@jabber.fr",body="text-only version",typ="message",payload=[f2fnode])
#client.send(message)
