#!/usr/bin/env python
from daemon import storage
print storage.config
from network import connect,message_handler
from time import sleep

with open("credentials.txt") as file:
    jid,password=file.readlines()[0].split()
print jid,password
client=connect(jid,password)
client.sendInitPresence()
client.RegisterHandler('message',message_handler)
while True:
    client.Process(1)
    sleep(1)
    
