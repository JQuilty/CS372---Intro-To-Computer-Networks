from socket import *

"""
John Quilty
Project 1, Program 1

Major works cited:
- Beej's Guide
- https://docs.python.org/3.8/howto/sockets.html
- https://docs.python.org/3/library/socket.html
- CS344 Code For Structure/Understanding
- https://stackoverflow.com/questions/28583565/str-object-has-no-attribute-decode-python-3-error
"""
#Set up the socket
siteSocket = socket(AF_INET, SOCK_STREAM)
#Using Port 80 for plain http
siteSocket.connect(("gaia.cs.umass.edu", 80))

#Sending the GET request exactly per the directions
requestedData = "GET /wireshark-labs/INTRO-wireshark-file1.html HTTP/1.1\r\nHost:gaia.cs.umass.edu\r\n\r\n"
#Sending and encoding, otherwise I get "TypeError: a bytes-like object is required, not 'str'"
siteSocket.send(requestedData.encode())

#Recieve data, convert to a string
responseData = siteSocket.recv(1024)
newResponse = str(responseData)

#Print the recieved data and attributes
print("Request: ", requestedData)
print("[RECV] - length: ", len(responseData))
print(responseData.decode())
