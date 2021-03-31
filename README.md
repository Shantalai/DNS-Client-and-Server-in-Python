# HTTP-DNS-Client-and-Server
Simplified implementation of DNS and HTTP client/server applications using Python

## DNS 
Using UDP sockets client program sends request to server to lookup IP address of a specified host in the domain. Server is responsible for the domain “student.test” represented by txt file. Server responds with type A resource record associated with the host. 
##### Example of output showing message format
```
$ python3 dns-client.py 127.0.0.1 9999 host1.student.test
Sending Request to 127.0.0.1, 9999:
Message ID: 57
Question Length: 23 bytes
Answer Length: 0 bytes
Question: host1.student.test A IN

Received Response from 127.0.0.1, 9999:
Return Code: 0 (No errors)
Message ID:   57
Question Length: 23 bytes
Answer Length: 41 bytes
Question: host1.student.test A IN
Answer: host1.student.test A IN 3600 192.168.10.1

```
## HTTP
Using TCP sockets client program uses HTTP protocol to fetch "web page" stored in file from server program using HTTP GET request and cache the response. It subsequently uses Conditional GET request to fetch the file again only if it was modified. 
##### Example of message format
##### Client request:
```
GET /filename.html HTTP/1.1\r\n
Host: localhost:12000\r\n
\r\n
```
##### Server response
```
HTTP/1.1 200 OK\r\n
Date: Sun, 04 Mar 2018 21:24:58 GMT\r\n
Last-Modified: Fri, 02 Mar 2018 21:06:02 GMT\r\n
Content-Length: 75\r\n
Content-Type: text/html; charset=UTF-8\r\n
\r\n
<html><p>First Line<br />Second Line<br />Third Line<br />COMPLETE<p><html>
```
