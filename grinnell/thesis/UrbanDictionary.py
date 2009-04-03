import re
import Browser
import codecs

from urllib import urlencode
from StringIO import StringIO

from lxml import etree
parser = etree.HTMLParser()

VOTES_PLACEHOLDER = -1337

def string_invalid(string):
    """A string is valid if and only if it contains only ASCII letters"""
    for char in string:
        if ord(char) > 128:
            return True
    return False

def lemma_page(lemma, page):
    """Given a lemma and page it returns the DOM for the page-th page of definitions for lemma"""
    q = {}
    q['page'] = page
    q['term'] = lemma
    result = Browser.fetch('http://www.urbandictionary.com/iphone/search?' + urlencode(q))
    # Transform all "br"s into newlines
    result = re.compile("\<br ?/?\>").sub("\n", result)
    return etree.parse(StringIO(result), parser)

def lemma_pages(lemma):
    page = lemma_page(lemma, 1)
    info = page.xpath("//div[@id='which_page']/text()")[0].strip('\n').split(' ')
    defs_on_one_page = int(info[1])
    all_defs = int(info[3])
    pages = int(all_defs / defs_on_one_page + 1)
    return pages

def statistics_for_lemma(lemma):
    """Given a lemma it returns ???"""

    result = {}
    def_ids = []

    pages = lemma_pages(lemma)
    for i in xrange(1, pages + 1):
        doc = lemma_page(lemma, i)
        # Get all the ids for the definitions
        def_ids_in_page = [ x.replace('entry_', '')
                            for x in doc.xpath("//div[@id='list_items']/div[@class='list_item']/div[@class='entry']/attribute::id") ]
        def_ids += def_ids_in_page

    # After we are done with fetching all the definition ids, fetch the votes (altogether)
    votes_regex = re.compile('Uncacheable.thumbs_update\(\{' +
                        '((' +
                        '"current_vote":""|' +
                        '"thumbs_up":(?P<up>[0-9]*)|' +
                        '"id":(?P<id>[0-9]*)|' +
                        '"thumbs_down":(?P<down>[0-9]*)' +
                        '),?)*' +
                        '\}\);')

    votes = Browser.fetch('http://www.urbandictionary.com/uncacheable.php?ids=' + ','.join(def_ids))

    total_votes_up = 0
    total_votes_down = 0

    for x in votes_regex.finditer(votes):
        def_id = x.group('id')
        votes_up = int(x.group('up'))
        votes_down = int(x.group('down'))
        total_votes_up += votes_up
        total_votes_down += votes_down

    result['count_defs'] = len(def_ids)
    result['total_votes_up'] = total_votes_up
    result['total_votes_down'] = total_votes_down
    result['total_votes'] = total_votes_up + total_votes_down

    return result
def lemma_page_expanded(lemma, page):
    """Given a lemma and page it returns the DOM for the page-th page of definitions for lemma"""
    q = {}
    q['page'] = page
    q['term'] = lemma
    result = Browser.fetch('http://www.urbandictionary.com/define.php?' + urlencode(q))
    # Transform all "br"s into newlines
    result = re.compile("\<br ?/?\>").sub("\n", result)
    return etree.parse(StringIO(result), parser)

def lemma_pages_expanded(lemma):
    page = lemma_page(lemma, 1)
    pages = int(page.xpath("//div[@id='paginator']/div/a[position() = last() - 1]/text()")[0])
    return pages
    
def statistics_for_lemma_expanded(lemma, PER_DEFINITION_DETAILS = False, PER_DEFINITION_DETAILS_EXPANDED = False):
    """Given a lemma it returns ???"""

    # PER_DEFINITION_DETAILS_EXPANDED presupposes PER_DEFINITION_DETAILS
    if PER_DEFINITION_DETAILS_EXPANDED:
        PER_DEFINITION_DETAILS = True
        
    result = {}
    def_ids = []
    
    pages = lemma_pages(lemma)
    for i in xrange(1, pages + 1):
        doc = lemma_page(lemma, i)
        # Get all the ids for the definitions
        def_ids_in_page = [ x.replace('tools_', '')
                            for x in doc.xpath("//td[@id='content']/table[@id='entries']/tr/td[@class='tools']/attribute::id") ]
        def_ids += def_ids_in_page

        if PER_DEFINITION_DETAILS:
            for def_id in def_ids_in_page:
                definition = {}

                if PER_DEFINITION_DETAILS_EXPANDED:
                    # Pick up the DOM only for the definition
                    definition_dom = doc.xpath("//td[@id='content']/table[@id='entries']/tr/td[@class='tools' and @id='tools_%s']/../following-sibling::tr[position() = 1]" % def_id)[0]
            
                    # Determine tags
                    definition['tags'] = definition_dom.xpath("./td[@class='text']/div[@class='greenery']/a[starts-with(@href, '/define.php?term=')]/text()")
            
                    # Determine author
                    author = definition_dom.xpath("./td[@class='text']/div[@class='greenery']/a[starts-with(@href, '/author.php?author=')]/text()")
                    if len(author) == 0:
                        author = "anonymous"
                    else:
                        author = author[0]
                    definition['author'] = author
            
                    # Determine date, if possible
                    date = definition_dom.xpath("./td[@class='text']/div[@class='greenery']/span[@class='date']/text()")
                    if len(date) == 0:
                        date = "unknown"
                    else:
                        date = date[0].strip()
                    definition['date'] = date

                definition['votes_up'] = VOTES_PLACEHOLDER
                definition['votes_down'] = VOTES_PLACEHOLDER
            
                result["defn_" + def_id] = definition
        
    # After we are done with fetching all the definition ids, fetch the votes (altogether)
    votes_regex = re.compile('Uncacheable.thumbs_update\(\{' +
                        '((' +
                        '"current_vote":""|' +
                        '"thumbs_up":(?P<up>[0-9]*)|' +
                        '"id":(?P<id>[0-9]*)|' +
                        '"thumbs_down":(?P<down>[0-9]*)' +
                        '),?)*' +
                        '\}\);')

    votes = Browser.fetch('http://www.urbandictionary.com/uncacheable.php?ids=' + ','.join(def_ids))

    total_votes_up = 0
    total_votes_down = 0
    
    for x in votes_regex.finditer(votes):
        def_id = x.group('id')
        votes_up = int(x.group('up'))
        votes_down = int(x.group('down'))
        if PER_DEFINITION_DETAILS:
            result["defn_" + def_id]['votes_up'] = votes_up
            result["defn_" + def_id]['votes_down'] = votes_down
        total_votes_up += votes_up
        total_votes_down += votes_down

    result['count_defs'] = len(def_ids)
    result['tags'] = lemma_page(lemma, 1).xpath("//td[@id='content']//span[@id='tags']/a/text()")
    result['total_votes_up'] = total_votes_up
    result['total_votes_down'] = total_votes_down
    result['total_votes'] = total_votes_up + total_votes_down

    return result

def words_page(character, page):
    params = {}
    params['character'] = character
    params['page'] = page
    return etree.parse(StringIO(Browser.fetch('http://www.urbandictionary.com/browse.php?' + urlencode(params))), parser)

def words_pages(character):
    page = words_page(character, 1)
    return int(page.xpath("//div[@id='paginator']/div/a[position() = last() - 1]/text()")[0])

def words_for_character(character):
    """Given a character it returns all the words in UrbanDictionary that start with this character via a generator"""    
    pages = words_pages(character)
    for i in xrange(1, pages + 1):
        page = words_page(character, i)
        for word in page.xpath("//table[@id='columnist']/tr/td/ul/li//a[starts-with(@href, '/define.php?term=')]/text()"):
            if not string_invalid(word):
                yield word

def words():
    """Returns all the words in UrbanDictionary. Use with caution."""
    alphabet = [ chr(i) for i in range(65, 65 + 26) ]
    for letter in alphabet:
        for word in all_words_for_character(letter):
            yield word