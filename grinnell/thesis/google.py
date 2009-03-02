from scrape import *

class SearchResults:
    def __init__(self, query, session=None):
        self.session = session or Session()
        self.lastindex = -1
        self.results = []
        self.query = query
        self.finished = 0
        self.hitcountpat = re.compile('Results')

    def __iter__(self):
        return self

    def __len__(self):
        if not self.results and not self.finished:
            self.fetch()
        return self.length

    def __getitem__(self, index):
        while index >= len(self.results):
            if self.finished:
                raise IndexError, index
            self.fetch()
        return self.results[index]

    def fetch(self):
        params = {}
        params['q'] = self.query
        params['num'] = 100
        params['start'] = len(self.results)
        params['safe'] = 'off'
        params['filter'] = 0
        code, headers, body = self.session.fetch(
            'http://google.com/search?' + urlencode(params))
        hitcount = td.get(body, content=self.hitcountpat)
        if not hitcount:
            self.finished = 1
            return
        words = striptags(hitcount).split()
        last = getnumber(words[words.index('-') + 1])
        self.length = getnumber(words[words.index('for') - 1])
        for start, end, attrs in p.findall(body, class_='g'):
            start, end = end, body.find('<!--n-->', end)
            entry = body[start:end]
            start, end, attrs = a.find(entry)
            url = attrs['href']
            title = entry[start:end]
            start, end, attrs = a.find(entry, content='Cached')
            cache = attrs and attrs.get('href')
            self.results.append((url, title, cache))
        if last == self.length:
            self.finished = 1
    
    def next(self):
        self.lastindex += 1
        while self.lastindex >= len(self.results) and not self.finished:
            self.fetch()
        if self.lastindex >= len(self.results) and self.finished:
            raise StopIteration
        return self[self.lastindex]

def search(query, session=None):
    return SearchResults(query, session)
