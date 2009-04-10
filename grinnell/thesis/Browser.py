import socket
socket.setdefaulttimeout(5)
import urllib2
import time

requests_count = 0
requests_time = time.time()
requests_threshold = 3 # requests / second (peaked at 6)

def fetch(target):
	  print (requests_count / requests_time)
    if (requests_count / requests_time) > requests_threshold:
        print "Slowing down..."
        time.sleep(1)
    try:
        return urllib2.urlopen(target).read()
    except (urllib2.HTTPError, urllib2.URLError):
        print "Retrying..."
        time.sleep(2)
        try:
            return urllib2.urlopen(target).read()
        except (urllib2.HTTPError, urllib2.URLError):
            print "Retrying... (for the last time)"
            time.sleep(2)
            return (urllib2.HTTPError, urllib2.URLError)
