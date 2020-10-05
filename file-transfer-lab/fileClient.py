#!/usr/bin/env python3
#Author: Ethan Benckwitz

import socket, sys, re
sys.path.append("../lib")       # for params
import params

from framedSock import framedSend, framedReceive

switchesVarDefaults = (
    (('-s', '--server'), 'server', "127.0.0.1:50001"),
    (('-d', '--debug'), "debug", False), # boolean (set if present)
    (('-?', '--usage'), "usage", False), # boolean (set if present)
    )

progname = "framedClient"
paramMap = params.parseParams(switchesVarDefaults)

server, usage, debug = paramMap["server"], paramMap["usage"], paramMap["debug"]

if usage:
    params.usage()

try:
    serverHost, serverPort = re.split(":", server)
    serverPort = int(serverPort)
except:
    print("Can't parse server:port from '%s'" % server)
    sys.exit(1)

addrFamily = socket.AF_INET
socktype = socket.SOCK_STREAM
addrPort = (serverHost, serverPort)

s = socket.socket(addrFamily, socktype)
if s is None:
    print('could not open socket')
    sys.exit(1)
    
print("Waiting to be connected...")
s.connect(addrPort)
print("Connected...")

while True:
    try:
        filename = input(str("Enter a file name to be transferred or enter exit: "))
        if filename == "exit": break
        sending = open(filename, "r")
        file_data = sending.read()
        if len(file_data) == 0: print("File was empty! Try a different file")
        framedSend(s, (file_data).encode(), debug)
        print("The file has been transferred successfully!")
    except FileNotFoundError:
        print("File Not Found!")

s.close()
