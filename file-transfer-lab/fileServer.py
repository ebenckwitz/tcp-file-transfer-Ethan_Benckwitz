#! /usr/bin/env python3
import socket, sys, re, os
sys.path.append("../lib")  # for params
import params
from os.path import exists

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
s.listen(5)              
# s is a factory for connected sockets
print("waiting to be connected...")


from framedSock import framedSend, framedReceive

while True:
    conn, addr = s.accept()  # wait until incoming connection request (and accept it)
    
    if not os.fork():
        while True:
            print('Connected by', addr)
            payload = ""
            try:
                filename = framedReceive(conn, debug)
            except:
                print("Could not transfer file")
                sys.exit(1)

            if debug: print("Received: ", payload)
            if payload is None:
                print("The contents in this file were empty!")
                sys.exit(1)

            fileContents = filename
            filename = filename.decode()
            if os.path.isfile("./SentFiles/" + filename):
                print("This file already exists on the server.")
                sys.exit(1)
            else:
                #try:
                #    payload = framedReceive(conn, debug)
                #except:
                #    print("Connection was lost while trying to receive data")
                #    sys.exit(0)
                #if debug: print("rec'd: ", payload)
                #if not payload:
                #    break
                writing = open("./SentFiles/" + filename, 'w+b')
                #payload = payload.decode()
                writing.write(fileContents)
                print(filename + "has been sent successfully!")
                #framedSend(conn, payload, debug)
                sys.exit(0)
                conn.close()
                writing.close()

'''
while True:
    sock, addr = s.accept()
    print("Connected to client", addr)
    if not os.fork():
        while True:
            payload = framedReceive(sock,debug)
            if not payload:
                break
            payload = payload.decode()
            
            if exists(payload):
                framedSend(sock, b"True", debug)
            else:
                framedSend(sock, b"False", debug)
                try:
                    payload2 = framedReceive(sock, debug)
                except:
                    print("Connection with client lost will receiving file data")
                    sys.exit(0)

                    if not payload2:
                        break
                    payload2 += b"!"
                    try:
                        framedSend(sock, payload2, debug)
                    except:
                        print("Connection lost with client while sending data.")

                    output = open("./SentFiles/" + payload, 'wb')
                    output.write(payload2)
                    print("All done!")
                    sock.close()

'''           

