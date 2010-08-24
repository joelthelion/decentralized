#!/usr/bin/env python
from daemon import storage
from network import connect,message_handler,presence_handler
from time import sleep

with open("credentials.txt") as file:
    jid,password=file.readlines()[0].split()
#print jid,password
client=connect(jid,password)
client.sendInitPresence()
client.RegisterHandler('presence',presence_handler)
client.RegisterDefaultHandler(message_handler)
while True:
    client.Process(1)
    sleep(1)
    
