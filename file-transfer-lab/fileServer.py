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
while True:
    filename = input(str("Please enter the name of the file that will save data or enter exit: "))
    if filename == "exit": sys.exit(1)
    with open(filename, "w") as writing:
        file_data = conn.recv(1024)
        udata = file_data.decode('utf-8')
        for l in udata:
            writing.write(l)
    print("Data has been sent successfully!")
    writing.close()
                 
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
