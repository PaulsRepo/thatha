import os
from UrbanDictionary import *

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
    f = open('data/words-%s' % i, 'r')
    lines_in_f = lines_in_file('data/defs-%s' % i)
    outf = open('data/defs-%s' % i, 'a')
    
    if lines_in_f != 0:
        for i in xrange(1, lines_in_f +1 ):
            f.readline()
            
    for word in f:
		try:
	        print word + "..."
	        word = word.strip()
	        r = get_definitions(word)
	        sss = ""
	        for j in r.keys():
	            if type(r[j]) == dict_type:
	               sss += ("%d/%d," % (int(r[j]['upvotes']), int(r[j]['downvotes'])))
	        out_string = "%s\t%d\t%d\t%d\t%s" % (word, r['count_defs'], r['total_upvotes'], r['total_downvotes'], sss)
	        print out_string
	        outf.write(out_string + '\n')
		except Exception:
			print "oopsie with " + word + ".... continuing"
        count += 1
        if count % 100 == 0:
            print count, " ", word