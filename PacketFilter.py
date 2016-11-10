#! /usr/bin/env python

import socket
from scapy.all import *

def getHost(ip):
    """
    This method returns the 'True Host' name for a
    given IP address
    """
    try:
        data = socket.gethostbyaddr(ip)
        host = repr(data[0])
        return host
    except Exception:
        # fail gracefully
        return False

src = set((p[IP].src) for p in PcapReader('output.pcap') if IP in p)
# IPlist = []
IPtoHostname = {}

for x in src:
    first, second, third, fourth = x.split('.')
    if int(third) >= 30 and int(third) <= 70:
        # IPlist.append(x)
		IPtoHostname[x] = getHost(x)
		

for k, v in IPtoHostname.iteritems():
    print k, v
