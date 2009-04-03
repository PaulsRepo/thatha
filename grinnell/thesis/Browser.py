import socket
socket.setdefaulttimeout(5)
import urllib2
import time

def fetch(target):
    try:
        return urllib2.urlopen(target).read().decode('utf-8')
    except (urllib2.HTTPError, urllib2.URLError):
        print "Retrying..."
        time.sleep(2)
        try:
            return urllib2.urlopen(target).read().decode('utf-8')
        except (urllib2.HTTPError, urllib2.URLError):
            print "Retrying... (for the last time)"
            time.sleep(2)
            return (urllib2.HTTPError, urllib2.URLError)
