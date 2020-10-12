#! /usr/bin/env python3
#@Author: Ethan Benckwitz

import socket, sys, re, os
sys.path.append("../lib")  # for params
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
s.listen(5)              # s is a factory for connected sockets
print("waiting to be connected...")
os.chdir("./SentFilesThread")

from threading import Thread;
from encapFramedSock import EncapFramedSock

class Server(Thread):
    def __init__(self, sockAddr):
        Thread.__init__(self)
        self.s, self.addr = sockAddr
        self.fs = EncapFramedSock(sockAddr)
    def run(self):
        print("New thread handling connection from", self.addr)
        while True:
            payload = ""
            try:
                filename, data = self.fs.receive(debug)
            except:
                print("Could not transfer file")
                sys.exit(1)
                
            if debug: print("Received: ", payload)
            if payload is None:
                print("The contents in this file were empty!")
                sys.exit(1)

            filename = filename.decode()
            if os.path.isfile(filename):
                print("This file already exists on the server.")
                sys.exit(1)
            else:
                writing = open(filename, 'w+b')
                writing.write(data)
                print("Data has been sent successfully!")
                writing.close()
                sys.exit(0)

while True:
    sockAddr = s.accept()  # wait until incoming connection request (and accept it)
    server = Server(sockAddr)
    server.start()




