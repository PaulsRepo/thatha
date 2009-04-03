import re
import Browser
import codecs

from urllib import urlencode
from StringIO import StringIO

from lxml import etree
parser = etree.HTMLParser()

def term_page(term, page):
    q = {}
    q['ie'] = 'UTF-8'
    q['start'] = page * 10
    q['q'] = term
    result = Browser.fetch('http://blogsearch.google.com/blogsearch?' + urlencode(q))
    return etree.parse(StringIO(result), parser)

def term_pages(term):
    page = term_page(term, 0)
    return int(page.xpath("//div[@id='navbar']/table/tr/td/a/text()")[-2])


def hits(phrase):
    # http://blogsearch.google.com/blogsearch?q=test
    return false
    
print term_pages('fagtard')