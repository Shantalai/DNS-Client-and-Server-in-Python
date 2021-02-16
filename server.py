#! /usr/bin/env python3
# DNS Server

import sys
import socket
import random
import time
import struct

# DNS storage, used dictionary with hostname for key
dnsTree = {}

# Read txt file into DNS storage
f = open("dns-master.txt", "r")
for i in range(4):
    skp=f.readline()
for l in f:
    if l.rstrip().startswith('#'):
        continue
    #split line into list to get hostname
    lst = l.rstrip().split(' ')
    #join the list back to form the answer string  
    dnsTree[lst.pop(0)] = " ".join(lst)

# Close file
f.close()

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])
mType = 2
rCode = 0
ipRes = 'non'

# Create a UDP socket. Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
# Assign server IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

print("The server is ready to receive on port:  " + str(serverPort) + "\n")

# loop forever listening for incoming UDP messages
while True:
    
    # Receive and print the client data from "data" socket
    data, address = serverSocket.recvfrom(1024)
    dnsHName=struct.unpack('!hhl',data[:8])
    
    #test output
    #print("Receive data from client " + address[0] + " "+str(address[1])+" " + str(dnsHName))
    #print(dnsHName[0])
    #print(dnsHName[1])
    #print(dnsHName[2])

    mIdrec = dnsHName[2]
    #rstr = dnsHName[3].decode('ascii').rstrip('\x00')
    rstr = data[8:].decode('ascii')
    
    #testing code
    print(rstr, " - rstr ", len(rstr), " type ", type(rstr))
    #print(rstr == 'host2.student.test')
    #print(len('host2.student.test'))

    if rstr in dnsTree:
        print(dnsTree[rstr])
        ipRes=dnsTree[rstr]
    else:
        print("notf")
        rCode = 1
    
    # Pack response data
    res1 = struct.pack('!hhl',mType, rCode, mIdrec)
    resData = res1+ipRes.encode('ascii')
    # Reset response code
    rCode = 0
    # Echo back to client
    print("Responding to mID:  request " + str(mIdrec))
    serverSocket.sendto(resData,address)
