#! /usr/bin/env python3
# HTTP Client
# Anastasia Kaliakova ak983
# Reference
import sys
import socket
import datetime, time
import os.path

# Get the server hostname, port and data length as command line arguments # localhost:12000/filename.html
url = sys.argv[1]
host = url.split(':')[0]
port = int(url.split('/')[0].split(':')[1])
url_file = url.split('/')[1]

# Build GET request 
GETrequest = "GET "+str(url_file)+" HTTP/1.1\r\n"+"Host: "+str(host)+":"+str(port)+"\r\n"

# Create client socket 
clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to server 
print("Connecting to " + host + ", " + str(port))
clientSocket.connect((host, port))

# Check if cache exists and last time was modified
try:
    secs = os.path.getmtime("cache.txt")
    t = time.gmtime(secs)
    last_mod_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT\r\n",t)
    #print(last_mod_time)
    lastModStr= "If-Modified-Since: "+last_mod_time

    # Send Conditional GET
    condGET= GETrequest+lastModStr
    print("Sending data to server: " + GETrequest)
    clientSocket.send(condGET.encode())

    # Receive the server response to Conditional GET
    #dataEcho = clientSocket.recv(len(data))
    dataEcho = clientSocket.recv(10000)

    # Get status code
    status= dataEcho.decode().split("\r\n")[0].split(" ")[1]
    #print("heerer status ",status)

    if(int(status)==200):
        # Write into client cache
        with open("cache.txt", "w") as f:
            f.write(dataEcho.decode())

    # Display the decoded server response as an output
    print("Receive data from server: \n" + dataEcho.decode())


except IOError:
    #print("no cache")

    # Send GET request
    print("Sending data to server:   " + GETrequest)
    clientSocket.send(GETrequest.encode())

    # Receive the server response to regular GET    
    #dataEcho = clientSocket.recv(len(data))
    dataEcho = clientSocket.recv(10000)

    # Display the decoded server response as an output
    print("Receive data from server: \n" + dataEcho.decode())

    # Get status code
    status= dataEcho.decode().split("\r\n")[0].split(" ")[1]
   #print("heerer was no file status ",status)

    if(int(status)==200):
        # Write into client cache
        with open("cache.txt", "w") as f:
            f.write(dataEcho.decode())


# Close the client socket
clientSocket.close()
