#! /usr/bin/env python3
# DNS Client
# Anastasia Kaliakova ak983
# Reference
# https://docs.python.org/3/library/socket.html#socket-objects
# https://www.kite.com/python/examples/5615/socket-handle-a-socket-timeout

import sys
import socket
import time
import random 
import datetime
import struct

# Get the server hostname, port and data length as command line arguments
host = sys.argv[1]
port = int(sys.argv[2])
hostname = str(sys.argv[3]) 
qLen = len(hostname.encode('utf-8'))
mType = 1
rCode = 0

# Create UDP client socket. Note the use of SOCK_DGRAM
clientsocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
clientsocket.settimeout(10)


for x in range(3):
    #Generate message ID
    randId = random.randint(0,100)
    
    # Pack data
    data1 = struct.pack('!hhl',mType, rCode,randId)
    data = data1+hostname.encode('ascii')

    # Print Request log
    print("Sending Request to " + str(host) + ", " + str(port) )
    print("Message ID: ",randId)
    print("Question Length: ", qLen)
    print("Answer Length: 0 bytes")
    print("Question: ", hostname, " A IN")
    print()
    
    # Send data to server
    clientsocket.sendto(data,(host, port))

    try:

        # Receive the server response
        dataEcho, address = clientsocket.recvfrom(port)
       
       # Fixed lenght part
        serverResponse = struct.unpack('!hhl',dataEcho[:8])
        resMType = serverResponse[0]
        resRCode = serverResponse[1]
        resMId = serverResponse[2]

        # Variable length part 
        strn = dataEcho[8:].decode('ascii')
        ansLen = len(strn.encode('utf-8'))
        
        # Print response log
        print("Recieved Response from  ",str(address[0])," ", str(address[1]))
        if(resRCode==0):
            print("Return code: ",str(resRCode)," (No errors)")
        elif(resRCode==1):
            print("Return code: ",str(resRCode)," (Name does not exist)")
        print("Message ID: ",str(resMId))
        print("Question Length: ", qLen)
        print("Answer Length: ", ansLen)
        print("Question: ", hostname, " A IN")
        if(resRCode==0):
            print("Answer: ", strn)
        print()
        print()
    except socket.timeout as e:
        print(e,"...")

#Close the client socket
clientsocket.close()
