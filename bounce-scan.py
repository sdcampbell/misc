#!/usr/bin/env python

# Import our libraries
import sys
import requests
from bs4 import BeautifulSoup

ipAddress =  sys.argv[1] # Get the IP address from the command line
url = "http://ports.yougetsignal.com/short-scan.php" # Self-explanatory
values = {"remoteAddress":ipAddress} # Our post value
r = requests.post(url, data=values) # Do the post
soup = BeautifulSoup(r.content, 'html.parser') # Use BeautifulSoup to parse html
print(soup.get_text()) # Strip html out and print text
