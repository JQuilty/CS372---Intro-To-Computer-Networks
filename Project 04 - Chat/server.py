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

#Get port if manually defined, otherwise go to the hard coded one
if len(sys.argv) == 2:
    serverPort = int(sys.argv[1])
else:
    serverPort = 21284

#Validate port setting
if (serverPort == None):
    print("Issue in port, terminating.\n")
    sys.exit()

#Make socket and bind per socket docs
chatServer = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#Make reusable per directions
chatServer.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
chatServer.bind(('localhost', serverPort))

#Start listening
chatServer.listen(1)
print("Server listening on localhost on port " + str(serverPort))
print("Waiting for message...")

#Make an object per accept() docs
chatClient = chatServer.accept()[0]

#Control variables
awaitingResponse = True

while (True):
    #Used when we are waiting the client to send
    if (awaitingResponse == True):
        #Recv and decode
        chatMessage = chatClient.recv(200).decode('utf-8')
        #Check for termination, if terminate, close sockets and exit
        if ("/q" in chatMessage):
            chatClient.close()
            chatServer.close()
            sys.exit()
        #Print message and flip awaitingResponse
        else:
            print("Client: " + chatMessage)
            awaitingResponse = False

    #Now we handle responses, get them, send, and flip awaitingResponse
    if (awaitingResponse == False):
        serverMessage = input("Your message: ")
        chatClient.send(serverMessage.encode('utf-8'))
        awaitingResponse = True
