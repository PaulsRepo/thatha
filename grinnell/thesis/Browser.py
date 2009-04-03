
import socket
socket.setdefaulttimeout(5)

import urllib2, time

def fetch_(target):
    try:
        return urllib2.urlopen(target).read().decode('utf-8')#.decode('utf-8')
    except (urllib2.HTTPError, urllib2.URLError):
        print "Retrying"
        time.sleep(2)
        return urllib2.urlopen(target).read().decode('utf-8')#.encode('utf-8')

def fetch(target):
    s = fetch_(target)
    return s

# import urllib2, urlparse, gzip
# from StringIO import StringIO