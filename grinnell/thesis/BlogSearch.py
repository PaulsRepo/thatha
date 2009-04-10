import re
import Browser
import codecs
import simplejson

from urllib import urlencode
from StringIO import StringIO

APIKEY = open('/home/athanasa/google_api_key', 'r').read().strip()

def search(query, **options):
	options.update({
		'v': '1.0',
		# http://code.google.com/apis/ajaxsearch/key.html
		'key': APIKEY,
		'q': '"%s"' % (query)
	})
	result = simplejson.JSONDecoder().decode(Browser.fetch('http://ajax.googleapis.com/ajax/services/search/blogs?' + urlencode(options)))
	return result['responseData']

def count(query):
	return int(search(query)['cursor']['estimatedResultCount'])
	