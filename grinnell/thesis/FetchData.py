import sys
import codecs
import UrbanDictionary

alphabet = [ chr(i) for i in range(65, 65 + 26) ]    

def calculate_alphabet_todo(list):
    import os
    result = [ i for i in list ]
    # Delete the last file, it is usually incomplete
    all_files = os.listdir('data/')
    to_delete = all_files[-1:]
    os.remove('data/' + to_delete[0])
    files = all_files[:-1]
    for f in files:
        if f.startswith('words-'):
            ignore, letter = f.split('words-')
            result.remove(letter)
    return result

def words_to_cache():
    print "Getting all words from UrbanDictionary..."
    count = 0
    alphabet_todo = calculate_alphabet_todo(alphabet)
    for letter in alphabet_todo:
        print "Letter: %s" % letter
        f = codecs.open('data/words-%s' % letter, 'w', 'UTF-8')
        for j in UrbanDictionary.words_for_character(letter):
            f.write(j + '\n')
            count += 1
            if count % 100 == 0:
                print count
                
def stop_remote():
    import mathlan
    mathlan.execute([ "killall python" for i in alphabet ])

def start_remote():
    import mathlan
#    mathlan.execute
#    'python /home/athanasa/thesis/get_data.py %s > /home/athanasa/thesis/data/logging-%s 2>&1 &' % (i,i)


def lines_in_file(x):
    try:
        f = open(x, 'r')
        count = 0
        for x in f: count += 1
        f.close()
        return count
    except Exception:
        return 0
    
def definitions_for_letter(i):
    count = 0
    dict_type = type({})

    print "letter:"+i
    f = open('/home/athanasa/thesis/data/words-%s' % i, 'r')
    lines_in_f = lines_in_file('data/defs-%s' % i)
    outf = open('/home/athanasa/thesis/data/defs-%s' % i, 'a')
    logf = open('/home/athanasa/thesis/data/logging-%s' % i, 'a')
    
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
            logf.write(out_string + '\n')
            logf.flush()
        outf.write(out_string + '\n')
        if count % 5 == 0:
            outf.flush()
        count += 1
        if count % 100 == 0:
            logf.write("%d %s %s\n" % (count, word, time.strftime('%x %X')))
            logf.flush()
        else:
            logf.write(".")

if len(sys.argv) == 2 and sys.argv[1] in alphabet:
    definitions_for_letter(sys.argv[1])