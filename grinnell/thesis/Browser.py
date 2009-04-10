import socket
socket.setdefaulttimeout(5)
import urllib2
import time

requests_count = 0
requests_time = time.time()
requests_threshold = 5

def fetch(target):
		global requests_count
		req = urllib2.Request(target, None, {'Referer': 'http://www.cs.grinnell.edu/~athanasa'})
		requests_count += 1
		rate = (requests_count / (time.time() - requests_time))
		if rate > requests_threshold:
				print "Slowing down..."
				time.sleep(1)
		try:
				return urllib2.urlopen(req).read()
		except (urllib2.HTTPError, urllib2.URLError):
				print "Retrying..."
				time.sleep(2)
				try:
						return urllib2.urlopen(target).read()
				except (urllib2.HTTPError, urllib2.URLError):
						print "Retrying... (for the last time)"
						time.sleep(2)
						return (urllib2.HTTPError, urllib2.URLError)
