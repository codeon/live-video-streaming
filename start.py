#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#       untitled.py
#       
#       Copyright 2011 Kapil Garg <kapilg@mastimaa>
#       
#       This program is free software; you can redistribute it and/or modify
#       it under the terms of the GNU General Public License as published by
#       the Free Software Foundation; either version 2 of the License, or
#       (at your option) any later version.
#       
#       This program is distributed in the hope that it will be useful,
#       but WITHOUT ANY WARRANTY; without even the implied warranty of
#       MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#       GNU General Public License for more details.
#       
#       You should have received a copy of the GNU General Public License
#       along with this program; if not, write to the Free Software
#       Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#       MA 02110-1301, USA.
import os
import sys
import socket
import struct
import numpy
import Image
import time

MYPORT = 8123
MYGROUP_4 = '224.0.0.251'
MYGROUP_6 = 'ff02::1:ff0a:9cd8'
group=MYGROUP_6
MYTTL = 1 # Increase to reach other networks

# This is the code for the server. It creates a socket and sends data across it using UDP protocol.

def server():
	# We shall first create the socket for connecting to the multicast address.
	addrinfo = socket.getaddrinfo(group, None)[0] 
	s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
	i=0
	while True:
		if i==0:
			data = Image.open('wow.jpg').tostring()
			s.sendto(data + '\0', (addrinfo[4][0], MYPORT))
			time.sleep(1)
			i+=1
		else:
			data = Image.open('ds.jpg').tostring()
			s.sendto(data + '\0', (addrinfo[4][0], MYPORT))
			time.sleep(1)

def client():
	addrinfo = socket.getaddrinfo(group, None)[0]
	s = socket.socket(addrinfo[0], socket.SOCK_DGRAM)
	s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	s.bind(('', MYPORT))
	group_bin = socket.inet_pton(addrinfo[0], addrinfo[4][0])
    # Join group
	mreq = group_bin + struct.pack('@I', 0)
	s.setsockopt(socket.IPPROTO_IPV6, socket.IPV6_JOIN_GROUP, mreq)
	i=0
	while True:
		data, sender = s.recvfrom(1500)
		while data[-1:] == '\0': data = data[:-1] # Strip trailing \0's
		image_recv=Image.fromstring('RGB', (16,16),data)
		if i==0:
			image_recv.save("wow2.jpg")
			i=i+1
		else:
			image_recv.save("ds4.jpg")
		
    
def main():
	
	if '-s' in sys.argv[1:]:
		server()
	else:
		client()
	return 0

if __name__ == '__main__':
	main()

