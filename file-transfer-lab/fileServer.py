#! /usr/bin/env python3
import socket, sys, re
sys.path.append("../lib")       # for params
import params

switchesVarDefaults = (
    (('-l', '--listenPort') ,'listenPort', 50001),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "echoserver"
paramMap = params.parseParams(switchesVarDefaults)

debug, listenPort = paramMap['debug'], paramMap['listenPort']
listenAddr = ''       # Symbolic name meaning all available interfaces

if paramMap['usage']:
    params.usage()

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
bindAddr = ("127.0.0.1", listenPort)
s.bind(bindAddr)
s.listen(1)              # allow only one outstanding request
# s is a factory for connected sockets

print("Waiting to be connected...")
conn, addr = s.accept()  # wait until incoming connection request (and accept it)
print('Connected by', addr)

#from framedSock import framedSend, framedReceive
filename = input(str("Please enter the name of the file: "))
f = open(filename, "wb")
file_data = f.read(1024)
conn.send(file_data)
print("Data has been sent successfully!")
                 
''''
while True:
    payload = framedReceive(sock, debug)
    if debug: print("rec'd: ", payload)
    if not payload:
        break
    payload += b"!"             # make emphatic!
    framedSend(sock, payload, debug)
'''
conn.close()
