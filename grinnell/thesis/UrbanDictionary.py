import re
# the order of the stuff in the array changes
regex = re.compile('Uncacheable.thumbs_update\(\{' +
                    '((' +
                    '"current_vote":""|' +
                    '"thumbs_up":(?P<up>[0-9]*)|' +
                    '"id":(?P<id>[0-9]*)|' +
                    '"thumbs_down":(?P<down>[0-9]*)' +
                    '),?)*' +
                    '\}\);')
                    
import Browser

from urllib import urlencode
from StringIO import StringIO
from lxml import etree
parser = etree.HTMLParser()
DEBUG = 1
def xpath_single(xxxx, string):
    r = xxxx.xpath(string)
    if len(r) != 1:
        raise Exception("invalid xpath result " + repr(r))
    else:
        return r[0]

def xpath(xxxx, string):
    return xxxx.xpath(string)

def get_definitions(lemma = 'fagtard'):
    def get_definitions_page(page = 1):
        q = {}
        q['page'] = page
        q['term'] = lemma
        result = Browser.fetch('http://www.urbandictionary.com/define.php?' + urlencode(q))
        #TODO
        result = result.replace("<br>", "").replace("<br />", "").replace("<br/>", "")
        return result

    def get_defdetails_from_doc(doc, dict):
#        definition_count = xpath(doc, "count(//td[@id='content']/table[@id='entries']/tr/td[@class='index'])")
        ids = [ x.replace('tools_', '')
                            for x in xpath(doc, "//td[@id='content']/table[@id='entries']/tr/td[@class='tools']/attribute::id") ]
        for defid in ids:
            definition = {}
            definition['id'] = defid
            defn = xpath_single(doc, "//td[@id='content']/table[@id='entries']/tr/td[@class='tools' and @id='tools_%s']/../following-sibling::tr[position() = 1]" % defid)
            definition['tags'] = xpath(defn, "./td[@class='text']/div[@class='greenery']/a[starts-with(@href, '/define.php?term=')]/text()")
            author = xpath(defn, "./td[@class='text']/div[@class='greenery']/a[starts-with(@href, '/author.php?author=')]/text()")
            if len(author) == 0:
                definition['author'] = "anonymous"
            elif len(author) == 1:
                definition['author'] = author[0]
            else:
                raise Exception('way too many authors')
            try:
                definition['date'] = xpath_single(defn, "./td[@class='text']/div[@class='greenery']/span[@class='date']/text()").strip()
            except Exception:
                definition['date'] = 'Unknown'
            definition['upvotes'] = 0
            definition['downvotes'] = 0
            dict[defid] = definition

        # http://www.urbandictionary.com/uncacheable.php?ids=1994953,123
        
    doc = etree.parse(StringIO(get_definitions_page(1)), parser)
    pages = xpath(doc, "//div[@id='paginator']/div/a[position() = last() - 1]/text()")
    if len(pages) == 0:
        pages = 1
    elif len(pages) == 1:
        pages = int(pages[0])
    else:
        raise Exception('invalid xpath result')
        
    tags = xpath(doc, "//td[@id='content']//span[@id='tags']/a/text()")
    d = {}
    get_defdetails_from_doc(doc, d)
    
    for i in xrange(2, pages + 1):
        doc = etree.parse(StringIO(get_definitions_page(i)), parser)
        get_defdetails_from_doc(doc, d)

    ids = d.keys()
    ajaxdata = Browser.fetch('http://www.urbandictionary.com/uncacheable.php?ids=' + ','.join(ids))

    total_upvotes = 0
    total_downvotes = 0
    
    for x in regex.finditer(ajaxdata):
        defid = x.group('id')
        upvotes = x.group('up')
        downvotes = x.group('down')
        d[defid]['upvotes'] = upvotes
        d[defid]['downvotes'] = downvotes
        total_upvotes += int(upvotes)
        total_downvotes += int(downvotes)

    d['count_defs'] = len(d)
    d['tags'] = tags
    d['total_upvotes'] = total_upvotes
    d['total_downvotes'] = total_downvotes
    d['total_votes'] = total_upvotes + total_downvotes
    
    
    return d

def get_all_words(character = 'A'):
    def get_all_words_page(page):
        params = {}
        params['character'] = character
        params['page'] = page
        doc = etree.parse(StringIO(Browser.fetch('http://www.urbandictionary.com/browse.php?' + urlencode(params))), parser)
        return doc
    
    doc = get_all_words_page(1)
    pages = int(xpath_single(doc, "//div[@id='paginator']/div/a[position() = last() - 1]/text()"))
    
    for i in xrange(1, pages + 1):
        if i != 1:
            doc = get_all_words_page(i)
        for j in xpath(doc, "//table[@id='columnist']/tr/td/ul/li//a[starts-with(@href, '/define.php?term=')]/text()"):
            yield j

def get_all_data():
    alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    count = 0
    for i in alphabet:
        print "Letter:" + i
        f = open('data/words-%s' % i, 'w')
        for j in get_all_words(i):
            f.write(j.encode('utf-8') + '\n')
            count += 1
            if count % 100 == 0:
                print count
