import sys
import codecs
import UrbanDictionary
import time
import urllib2

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
            if not j.endswith("..."):
                f.write(j + '\n')
                count += 1
                if count % 100 == 0:
                    print count
                
def stop_remote():
    import mathlan
    mathlan.execute([ "killall python" for i in alphabet ])

def start_remote():
    import mathlan
    mathlan.execute([ "cd thesis && python FetchData.py %s &" % (i) for i in alphabet ])


def file_lines(filename):
    try:
        f = open(filename, 'r')
        count = 0
        for x in f: count += 1
        f.close()
        return count
    except Exception:
        return 0
    
def stats_for_letter_to_cache(letter):
    total_words = file_lines('data/words-%s' % letter)
    
    print "Letter: %s" % letter
    
    words = codecs.open('data/words-%s' % letter, 'r', 'UTF-8')
    stats = codecs.open('data/stats-%s' % letter, 'a', 'UTF-8')
    logging = open('data/logging-%s' % letter, 'a')
    
    already_statted = file_lines('data/stats-%s' % letter)
    
    if already_statted != 0:
        # Skip already_statted lines from words since they are already processed
        for i in xrange(1, already_statted + 1):
            words.readline()
        logging.write("Skipped %d lines since they are already processed\n" % already_statted)
    else:
        # We are just beginning this file, write the header
        stats.write("lemma\tdefinitions\tvotes_up\tvotes_down\tvotes_total\n")
    
    count = already_statted
    
    for word in words:
        word = word.strip()
        count += 1 
        try:
            info = UrbanDictionary.statistics_for_lemma(word)
            out_string = "%s\t%d\t%d\t%d\t%d\n" % (word, info['count_defs'], info['total_votes_up'], info['total_votes_down'], info['total_votes'])
            stats.write(out_string)
        except urllib2.URLError, urllib2.HTTPError:
            logging.write("FAILED: %s\n" % word)
            logging.flush()
            stats.write("%s\tFAILED\n" % word)
        
        if count % 10 == 0:
            stats.flush()
            percentage = (float(count) / total_words) * 100
            logging.write("Processed %6d out of %6d || letter: %s || %2.2f || %s || %s\n" % (count, total_words, letter, percentage, time.strftime('%x %X'), word))
            logging.flush()

if len(sys.argv) == 2 and sys.argv[1] in alphabet:
    stats_for_letter_to_cache(sys.argv[1])
