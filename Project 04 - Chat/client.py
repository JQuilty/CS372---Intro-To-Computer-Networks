"""
John Quilty
CS372
Chat Project

Resources Cited:
- Beej
- https://docs.python.org/3/library/socket.html
- https://docs.python.org/3/library/socket.html#socket.socket.listen
- https://docs.python.org/3/library/socket.html#socket.socket.recv
- https://realpython.com/python-sockets/
"""

import socket
import sys

#Set variable to None
serverPort = None

#Get ports if manually defined, otherwise go to the hard coded one
if len(sys.argv) == 2:
    serverPort = int(sys.argv[1])
else:
    serverPort = 21284

#Validate port
if (serverPort == None):
    print("Issue in port, terminating.\n")
    sys.exit()

#Make socket and connect per docs
serverConnection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverConnection.connect(('localhost', serverPort))

#Validate connection and socket creation
if serverConnection:
    print("Connected, you may send your message.\n")
else:
    print("Error establishing socket. Aborting.")
    sys.exit()

#Control variables
awaitingResponse = False

while (True):
    #Recieving message
    if (awaitingResponse == True):
        #Recieve and decode, print, then flip awaitingResponse
        chatMessage = serverConnection.recv(200).decode('utf-8')
        print("Server: " + str(chatMessage))
        awaitingResponse = False

    #Sending message
    if (awaitingResponse == False):
        #Get input, send, encode
        clientMessage = input("Your message: ")
        serverConnection.send(clientMessage.encode('utf-8'))

        #Checking for termination, if so close socket and exit
        if ("/q" in clientMessage):
            serverConnection.close()
            sys.exit()

        #Flip awaitingResponse
        awaitingResponse = True
