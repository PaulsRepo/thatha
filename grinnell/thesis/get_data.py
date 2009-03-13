import sys
import os
from UrbanDictionary import *
import urllib2

alphabet = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']

def lines_in_file(x):
    try:
        f = open(x, 'r')
        count = 0
        for x in f: count += 1
        f.close()
        return count
    except Exception:
        return 0
    
def get_defs(i):
    count = 0
    dict_type = type({})

    print "letter:"+i
    f = open('/home/athanasa/thesis/data/words-%s' % i, 'r')
    lines_in_f = lines_in_file('data/defs-%s' % i)
    outf = open('/home/athanasa/thesis/data/defs-%s' % i, 'a')
    
    if lines_in_f != 0:
        for i in xrange(1, lines_in_f +1 ):
            f.readline()
            
    for word in f:
        word = word.strip()
        try:
            r = get_definitions(word)
            sss = ""
            for j in r.keys():
                if type(r[j]) == dict_type:
                    sss += ("%d/%d," % (int(r[j]['upvotes']), int(r[j]['downvotes'])))
            out_string = "%s\t%d\t%d\t%d\t%s" % (word, r['count_defs'], r['total_upvotes'], r['total_downvotes'], sss)
        except (urllib2.URLError, urllib2.HTTPError):
            out_string = "%s\tFAILED" % word
            print out_string
        outf.write(out_string + '\n')
        if count % 5 == 0:
            outf.flush()
        count += 1
        if count % 100 == 0:
            print count, " ", word
        else:
            print ".",
            
if sys.argv[1] in alphabet:
    get_defs(sys.argv[1])