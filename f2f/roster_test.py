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
