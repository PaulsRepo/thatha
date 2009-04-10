import re
import Browser
import codecs
import simplejson

from urllib import urlencode
from StringIO import StringIO

# from lxml import etree
# sparser = etree.HTMLParser()

def search(query, **options):
	options.update({
		'v': '1.0',
		'q': '"%s"' % (query)
	})
	result = simplejson.JSONDecoder().decode(Browser.fetch('http://ajax.googleapis.com/ajax/services/search/blogs?' + urlencode(options)))
	return result['responseData']

def count(query):
	return int(search(query)['cursor']['estimatedResultCount'])
	