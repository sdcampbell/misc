#!/usr/bin/env python

"""
Author:  Steve Campbell, @campbellstevend, sdcampbell68@live.com
Purpose: This script takes an input list of domain names and
         enumerates the IP address, URL after redirect, web page
         title, server, and X-Powered-By info and outputs to csv.
"""


import sys
import subprocess
import requests
import csv
import socket
from bs4 import BeautifulSoup

def getNetblockCustomerName(IP):
    cmd = "whois %s | grep NetName | head -1 | tr -s ' ' | cut -d' ' -f 2-" % IP
    name = subprocess.check_output(cmd, shell=True)
    return name.rstrip('\r\n')


def getIP(domain):
    try:
        IP = socket.gethostbyname(domain)
        return IP
    except:
        return ""

def getURL(domain):
    urlstr = "http://" + domain
    try:
        r = requests.get(urlstr)
        page = r.text
        soup = BeautifulSoup(page, 'html.parser')
        url = r.url
        title = soup.title.string.encode('utf-8').strip()
        server = str(r.headers['Server'])
    except:
        url = ""
        title = ""
        server = ""
    try:
        poweredby = str(r.headers['x-powered-by'])
    except:
        poweredby = ""
    return (url, title, server, poweredby)
    
    

if __name__ == '__main__':

    usage = 'Error, Correct Usage: program.py "/path/to/input.txt" "/path/to/output.txt"'

    if (len(sys.argv) < 3):
        print(usage)
        sys.exit()

    else:
        domains = open((sys.argv[1]), 'r')
        outfile = open((sys.argv[2]), 'w')
        writer = csv.writer(outfile)

        writer.writerow(['Domain Name', 'IP Address', 'Net Block Owner', 'Redirect or Error', 'Title', 'Server', 'Powered By'])

        for x in domains:
            domain = x.rstrip('\r\n')
            IP = getIP(domain)
            if IP == "":
                writer.writerow([domain,"NotFound"])
                continue
            else:
                NetblockOwner = getNetblockCustomerName(IP)
                URL, Title, Server, PoweredBy = getURL(domain)
                # print domain, IP, NetblockOwner, URL, Title, Server, PoweredBy
                writer.writerow([domain, IP, NetblockOwner, URL, Title, Server, PoweredBy])
            
        
        domains.close()
        outfile.close()


