from socket import *
from random import randint

"""
John Quilty
Project 1, Program 3

Works cited:
- Beej's Guide
- https://docs.python.org/3.8/howto/sockets.html
- https://docs.python.org/3/library/socket.html
- CS344 Code For Structure/Understanding
- https://stackoverflow.com/questions/28583565/str-object-has-no-attribute-decode-python-3-error
"""

#Data from the instructions
data = "HTTP/1.1 200 OK\r\n"\
"Content-Type: text/html; charset=UTF-8\r\n\r\n"\
"<html>Congratulations! You've downloaded the first Wireshark lab file!</html>\r\n"

#Set the IP and get the port. Port is randomized in range per instructions.
#IP is set to loopback.
serverIP = "127.0.0.1"
serverPort = randint(1024, 65535)

#Set up the IP/port and bind per Socket docs
hostServer = socket(AF_INET, SOCK_STREAM)
hostServer.bind((serverIP, serverPort))

#Start listening
hostServer.listen(1)

#Print initial info
print("Connected by ('%s', %d)\n" % (serverIP, serverPort))

#Accept a connection
clientBrowser = hostServer.accept()[0]

#Variable to count how many bytes we've recieved
bytes_recieved = 0

#While loop while we await a connection
while True:
    #Recieve data, decode it, and check for how much was recieved
    responseData = clientBrowser.recv(1024)
    responseData = responseData.decode()
    bytes_recieved = len(responseData)

    #If it recieves a connection, print out the data per instructions,
    #send encoded data, then close socket and break the loop, terminating
    #the program.
    if (bytes_recieved > 0):
        print("Recieved: ", responseData.encode(), "\n")
        print("Sending>>>>>>>")
        print(data)
        print("<<<<<<<")
        clientBrowser.send(data.encode())
        clientBrowser.close()
        break
