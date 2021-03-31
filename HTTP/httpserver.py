#! /usr/bin/env python3
# HTTP Server
# Anastasia Kaliakova ak983
# Reference
 
import sys
import socket
import datetime, time
import os.path

# Read server IP address and port from command-line arguments
serverIP = sys.argv[1]
serverPort = int(sys.argv[2])

dataLen = 1000000

# Create server socket TCP 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Assign IP address and port number to socket
serverSocket.bind((serverIP, serverPort))

# Listen for incoming connection requests
serverSocket.listen(1)

print('The server is ready to receive on port:  ' + str(serverPort) + '\n')

while True:
    # Accept incoming connection requests; allocate a new socket for data communication
    connectionSocket, address = serverSocket.accept()
    print("Socket created for client " + address[0] + ", " + str(address[1]))

    # Receive and print the client data in bytes from "data" socket
    data = connectionSocket.recv(dataLen).decode()
    print("Data from client: \n" + data)

    dataList = data.split('\r\n')
    # Read request line of GET request
    reqLine= dataList[0].split(' ')
    method= reqLine[0]
    objectFile= reqLine[1]
    version= reqLine[2]

    # Read host line of GET

    # Get current time and date
    ct = datetime.datetime.now(datetime.timezone.utc)
    curDate = ct.strftime("%a, %d %b %Y %H:%M:%S %Z") 

    # Check if file exists and read in html file 
    HTTPresponce= ""
    body = ""
    statusCode= 404
    statusPhr= "Not Found"
    try:
        with open(objectFile, "r") as myfile:
            body = "".join(myfile.readlines())

        bodyLen = len(body)
        statusCode= 200
        statusPhr= "OK"
        # Get last modified date of data file
        secs = os.path.getmtime(objectFile)
        t = time.gmtime(secs)
        file_mod_time = time.strftime("%a, %d %b %Y %H:%M:%S GMT\r\n",t)
        #print("Last mod time on data file ",file_mod_time)

        # Handle Conditional GET
        if(len(dataList)>3):
            # Read If-Modified-Since line of Conditional GET
            clientDate= dataList[2][19:]+"\r\n"
            
            #print("conditional GET date of client ",clientDate)
            file_date= time.strptime(file_mod_time, "%a, %d %b %Y %H:%M:%S %Z\r\n")
            client_date= time.strptime(clientDate, "%a, %d %b %Y %H:%M:%S %Z\r\n")
            if(client_date<file_date):
                #print("file was updated ")
                HTTPresponce= version+" "+str(statusCode)+" "+statusPhr+" "+"\r\n"+"Date "+curDate+"\r\n"+"Content-Length: "+str(bodyLen)+"\r\n"+"Content-Type: text/html; charset=UTF-8\r\n"+"\r\n"+body
            else:
                #print("file was not updated")
                statusCode= 304
                statusPhr= "Not Modified"
                HTTPresponce= version+" "+str(statusCode)+" "+statusPhr+" "+"\r\n"+"Date "+curDate+"\r\n"+"\r\n"
        else:
            HTTPresponce= version+" "+str(statusCode)+" "+statusPhr+" "+"\r\n"+"Date "+curDate+"\r\n"+"Content-Length: "+str(bodyLen)+"\r\n"+"Content-Type: text/html; charset=UTF-8\r\n"+"\r\n"+body
    except IOError:
        #print("File does not exists")
        HTTPresponce= version+" "+str(statusCode)+" "+statusPhr+" "+"\r\n"+"Date "+curDate+"\r\n"+"Content-Length: 0"+"\r\n"+"\r\n"


    # Echo back to client
    connectionSocket.send(HTTPresponce.encode())