
# Adapted from companion material available for the textbook Computer Networking: A Top-Down Approach, 6th Edition
# Kurose & Ross ©2013

"""
John Quilty
CS372 - Project 3

Works Cited/Consulted:
- https://stackoverflow.com/questions/34614893/how-is-an-icmp-packet-constructed-in-python
- Kurose book
- Beej
- Python Networking Docs -- https://docs.python.org/3.8/howto/sockets.html
- https://docs.python.org/2/library/struct.html
- https://sira.dev/2019/06/24/layer-2-socket-programming.html
- https://piazza.com/class/k892xt0vqjs3x5?cid=234
- https://piazza.com/class/k892xt0vqjs3x5?cid=229
- https://piazza.com/class/k892xt0vqjs3x5?cid=264
- https://piazza.com/class/k892xt0vqjs3x5?cid=249
- https://www.geeksforgeeks.org/struct-module-python/
- http://sock-raw.org/papers/sock_raw
"""

from socket import *
import os
import sys
import struct
import time
import select
import binascii
import random

ICMP_ECHO_REQUEST = 8
MAX_HOPS = 30
TIMEOUT  = 2.0
TRIES    = 2

def checksum(string):
	csum = 0
	countTo = (len(string) // 2) * 2

	count = 0
	while count < countTo:
		#I got rid of the ord calls per piazza
		thisVal = string[count+1] * 256 + string[count]
		csum = csum + thisVal
		csum = csum & 0xffffffff
		count = count + 2

	if countTo < len(string):
		csum + string[len(string) - 1]
		csum = csum & 0xffffffff

	csum = (csum >> 16) + (csum & 0xffff)
	csum = csum + (csum >> 16)
	answer = ~csum
	answer = answer & 0xffff
	answer = answer >> 8 | (answer << 8 & 0xff00)
	return answer

def build_packet(data_size):
	# First, make the header of the packet, then append the checksum to the header,
	# then finally append the data

	# Don’t send the packet yet, just return the final packet in this function.
	# So the function ending should look like this
	# Note: padding = bytes(data_size)
	#Making some dummy values for later
	dummyChecksum = 0
	myChecksum = 0

	#Making and encoding data
	packetData = "This is data"
	packetData_bytes = str.encode(packetData)

	#padding
	padding = bytes(data_size)

	#For the ID part I'm just going to get something random that's still within two bytes
	id = random.randrange(1, 256)
	
	#Assemble using struct.pack
	#Mostly consulting this: https://docs.python.org/2/library/struct.html
	#Someone on slack also suggested filling it with dummy data for the header at first then again with the real checksum
	header = struct.pack("!bbHHh", ICMP_ECHO_REQUEST, 0, dummyChecksum, id, 1)
	realCheckSum = checksum(header + packetData_bytes)
	header = struct.pack("!bbHHh", ICMP_ECHO_REQUEST, 0, realCheckSum, id, 1)
	
	#Make packet and return
	packet = header + packetData_bytes + padding
	return packet

def get_route(hostname,data_size):
	timeLeft = TIMEOUT
	for ttl in range(1,MAX_HOPS):
		for tries in range(TRIES):

			destAddr = gethostbyname(hostname)

			# SOCK_RAW is a powerful socket type. For more details:   http://sock-raw.org/papers/sock_raw
			#Fill in start
			# Make a raw socket named mySocket
			#Fill in end
			#Using IPPROTO_ICMP
			mySocket = socket(AF_INET, SOCK_RAW, IPPROTO_ICMP)

			# setsockopt method is used to set the time-to-live field.
			mySocket.setsockopt(IPPROTO_IP, IP_TTL, struct.pack('I', ttl))
			mySocket.settimeout(TIMEOUT)
			try:
				d = build_packet(data_size)
				mySocket.sendto(d, (hostname, 0))
				t= time.time()
				startedSelect = time.time()
				whatReady = select.select([mySocket], [], [], timeLeft)
				howLongInSelect = (time.time() - startedSelect)
				if whatReady[0] == []: # Timeout
					print("  *        *        *    Request timed out.")
				recvPacket, addr = mySocket.recvfrom(1024)
				timeReceived = time.time()
				timeLeft = timeLeft - howLongInSelect

				#I changed this to return based on this piazza thread: https://piazza.com/class/k892xt0vqjs3x5?cid=249
				if timeLeft <= 0:
					print("  *        *        *    Request timed out.")
					return

			except timeout:
				continue

			else:
				#Fill in start
				#Fetch the icmp type from the IP packet
				#Fill in end             

				#Unpack everything, I consulted this Piazza thread: https://piazza.com/class/k892xt0vqjs3x5?cid=264   
				types, code, checksum, ID, sequence = struct.unpack("bbHHh", (recvPacket[20:28]))
				
				if types == 11:
					bytes = struct.calcsize("d")
					timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
					print("  %d    rtt=%.0f ms    %s" %(ttl, (timeReceived -t)*1000, addr[0]))

				elif types == 3:
					bytes = struct.calcsize("d")
					timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
					print("  %d    rtt=%.0f ms    %s" %(ttl, (timeReceived-t)*1000, addr[0]))

				elif types == 0:
					bytes = struct.calcsize("d")
					timeSent = struct.unpack("d", recvPacket[28:28 + bytes])[0]
					#Modified the skeleton code based on this: https://piazza.com/class/k892xt0vqjs3x5?cid=239
					print("  %d    rtt=%.0f ms    %s" %(ttl, (timeReceived - t)*1000, addr[0]))
					return

				else:
					print("error")
				break
			finally:
				mySocket.close()



print('Argument List: {0}'.format(str(sys.argv)))

data_size = 0
if len(sys.argv) >= 2:
	data_size = int(sys.argv[1])

print("traceroute: oregonstate.edu, North America")
get_route("oregonstate.edu",data_size)
print("traceroute: gaia.cs.umass.edu, North America")
get_route("gaia.cs.umass.edu",data_size)
print("traceroute: UK Parliament, Europe")
get_route("parliament.uk", data_size)
print("traceroute: Australian Broadcasting Corporation, Australia")
get_route("abc.net.au", data_size)