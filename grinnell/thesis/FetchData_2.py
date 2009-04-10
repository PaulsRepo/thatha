import sys
import codecs
import time
import BlogSearch
import os

alphabet = [ chr(i) for i in range(65, 65 + 26) ]    

def file_lines(filename):
    try:
        f = open(filename, 'r')
        count = 0
        for x in f: count += 1
        f.close()
        return count
    except Exception:
        return 0

def stop_remote():
    import mathlan
    mathlan.execute([ "killall python" for i in alphabet ])

def start_remote():
    import mathlan
    mathlan.execute([ "cd thesis && python FetchData_2.py %s &" % (i) for i in alphabet ])

def google_for_letter_to_cache(letter):
    total_words = file_lines('data/words-%s' % letter)

    print "Letter: %s" % letter

    words = codecs.open('data/words-%s' % letter, 'r', 'UTF-8')
    stats = codecs.open('data/goog-%s' % letter, 'a', 'UTF-8')
    logging = open('data/logging-goog-%s' % letter, 'a')

    already_statted = file_lines('data/goog-%s' % letter)

    if already_statted != 0:
        # Skip already_statted lines from words since they are already processed
        for i in xrange(1, already_statted + 1):
            words.readline()
        logging.write("Skipped %d lines since they are already processed\n" % already_statted)
    else:
        # We are just beginning this file, write the header
        stats.write("lemma\tblogsearch\n")

    count = already_statted

    for word in words:
        word = word.strip()
        count += 1 
        try:
            info = BlogSearch.count(word)
            out_string = "%s\t%d\n" % (word, info)
            stats.write(out_string)
        except:
            logging.write("FAILED: %s\n" % word)
            logging.flush()
            stats.write("%s\tFAILED\n" % word)
        if count % 10 == 0:
            stats.flush()
            percentage = (float(count) / total_words) * 100
            logging.write("Processed %6d out of %6d || letter: %s || %2.2f || %s || %s\n" % (count, total_words, letter, percentage, time.strftime('%x %X'), word))
            logging.flush()
    logging.write("Letter %s || DONE\n" % letter)
    logging.flush()

if len(sys.argv) == 2:
	if sys.argv[1] in alphabet:
		google_for_letter_to_cache(sys.argv[1])
