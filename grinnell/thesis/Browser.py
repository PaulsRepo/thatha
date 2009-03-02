# http://www.urbandictionary.com/define.php?page=2&term=freedom+fries

#import httplib
#httplib.HTTPConnection.debuglevel = 1
import socket
socket.setdefaulttimeout(10)

import urllib2, time
#data = urllib2.urlopen('http://www.urbandictionary.com/define.php?page=2&term=freedom+fries').read()
# print data
#import sys

def fetch(target):
    # http://www.diveintopython.org/http_web_services/
    try:
        return urllib2.urlopen(target).read()
    except urllib2.URLError:
        print "Retrying"
        time.sleep(2)
        return urllib2.urlopen(target).read()        
    except urllib2.HTTPError:
        print "Retrying"
        time.sleep(2)
        return urllib2.urlopen(target).read()
        
    
# import urllib2, urlparse, gzip
# from StringIO import StringIO
