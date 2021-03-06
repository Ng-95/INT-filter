#!/usr/bin/env python
import argparse
import sys
import socket
import random
import struct
import time
import redis

from scapy.all import sendp, send, get_if_list, get_if_hwaddr, get_if_addr
from scapy.all import Packet
from scapy.all import Ether, IP, UDP, TCP

sleep_time = 0.1


def get_if():
	ifs = get_if_list()
	iface = None  # "h1-eth0"
	for i in get_if_list():
		if "eth0" in i:
			iface = i
			break;
	if not iface:
		print
		"Cannot find eth0 interface"
		exit(1)
	return iface


def main():
	iface = get_if()
	source = get_if_hwaddr(iface)

	# data database
	r4 = redis.Redis(unix_socket_path='/var/run/redis/redis.sock', db=3)

	if source == '00:00:00:01:01:01':

		while True:
			r4.incr('send')
			pkt = Ether(src=source, dst='00:00:00:02:01:02', type=1792)
			pkt = pkt / '\x00\x00' / '\x00\x01' / '\x00\x01' / '\x00\x02' / '\x00\x03' / '\x80\x04' / '\x07\x01' / '\x00\x00'
			# r4.set('send',int(r4.get('send'))+1)
			sendp(pkt, iface=iface, verbose=False)
			time.sleep(sleep_time)

	elif source == '00:00:00:01:01:02':

		while True:
			r4.incr('send')
			pkt = Ether(src=source, dst='00:00:00:02:02:01', type=1792)
			pkt = pkt / '\x00\x00' / '\x00\x02' / '\x00\x02' / '\x00\x02' / '\x00\x04' / '\x80\x03' / '\x07\x01' / '\x00\x00'
			# r4.set('send',int(r4.get('send'))+1)
			sendp(pkt, iface=iface, verbose=False)
			time.sleep(sleep_time)

	elif source == '00:00:00:01:02:01':

		while True:
			r4.incr('send')
			pkt = Ether(src=source, dst='00:00:00:02:02:02', type=1792)
			pkt = pkt / '\x00\x00' / '\x00\x01' / '\x00\x02' / '\x00\x02' / '\x00\x04' / '\x80\x04' / '\x07\x01' / '\x00\x00'
			# r4.set('send',int(r4.get('send'))+1)
			sendp(pkt, iface=iface, verbose=False)
			time.sleep(sleep_time)

	elif source == '00:00:00:01:02:02':

		while True:
			r4.incr('send')
			pkt = Ether(src=source, dst='00:00:00:02:01:01', type=1792)
			pkt = pkt / '\x00\x00' / '\x00\x02' / '\x00\x01' / '\x00\x02' / '\x00\x03' / '\x80\x03' / '\x07\x01' / '\x00\x00'
			# r4.set('send',int(r4.get('send'))+1)
			sendp(pkt, iface=iface, verbose=False)
			time.sleep(sleep_time)

	elif source == '00:00:00:02:01:01':

		while True:
			r4.incr('send')
			pkt = Ether(src=source, dst='00:00:00:01:02:02', type=1792)
			pkt = pkt / '\x00\x00' / '\x00\x02' / '\x00\x01' / '\x00\x01' / '\x00\x04' / '\x80\x04' / '\x07\x01' / '\x00\x00'
			# r4.set('send',int(r4.get('send'))+1)
			sendp(pkt, iface=iface, verbose=False)
			time.sleep(sleep_time)   

	elif source == '00:00:00:02:01:02':

		while True:
			r4.incr('send')
			pkt = Ether(src=source, dst='00:00:00:01:01:01', type=1792)
			pkt = pkt / '\x00\x00' / '\x00\x01' / '\x00\x01' / '\x00\x01' / '\x00\x03' / '\x80\x03' / '\x07\x01' / '\x00\x00'
			# r4.set('send',int(r4.get('send'))+1)
			sendp(pkt, iface=iface, verbose=False)
			time.sleep(sleep_time)

	elif source == '00:00:00:02:02:01':

		while True:
			r4.incr('send')
			pkt = Ether(src=source, dst='00:00:00:01:01:02', type=1792)
			pkt = pkt / '\x00\x00' / '\x00\x02' / '\x00\x02' / '\x00\x01' / '\x00\x03' / '\x80\x04' / '\x07\x01' / '\x00\x00'
			# r4.set('send',int(r4.get('send'))+1)
			sendp(pkt, iface=iface, verbose=False)
			time.sleep(sleep_time)

	elif source == '00:00:00:02:02:02':

		while True:
			r4.incr('send')
			pkt = Ether(src=source, dst='00:00:00:01:02:01', type=1792)
			pkt = pkt / '\x00\x00' / '\x00\x01' / '\x00\x02' / '\x00\x01' / '\x00\x04' / '\x80\x03' / '\x07\x01' / '\x00\x00'
			# r4.set('send',int(r4.get('send'))+1)
			sendp(pkt, iface=iface, verbose=False)
			time.sleep(sleep_time)




if __name__ == '__main__':
	main()
