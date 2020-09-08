from socket import *

"""
John Quilty
Project 1, Program 2

Works cited:
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
requestedData = "GET /wireshark-labs/HTTP-wireshark-file3.html HTTP/1.1\r\nHost:gaia.cs.umass.edu\r\n\r\n"
#Sending and encoding, otherwise I get "TypeError: a bytes-like object is required, not 'str'"
siteSocket.send(requestedData.encode())

#Variables to hold and process our recieved data
newResponse = ""
total_bytes = 0
bytes_recieved = 0

#While loop will run and recieve data, once it gets nothing, it breaks
while (True):
    #Recieve data, decode, measure it
    responseData = siteSocket.recv(1024)
    responseData = responseData.decode()
    bytes_recieved = len(responseData)

    #If there's data, append to the string, increase our byte count
    if (bytes_recieved > 0):
        newResponse += str(responseData)
        total_bytes += len(responseData)

    #Break if there's no more data to recieve
    else:
        break

#Print everything out
print("Request: ", requestedData)
print("[RECV] - length: ", str(len(newResponse)))
print(newResponse)
