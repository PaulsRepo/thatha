#!/usr/bin/python
import os

print "ALTER TABLE ud ADD blogsearch int;"


count = 0
for file in os.listdir('data/'):
	if file.startswith('goog-'):
		f = open('data/' + file, 'r')
		f.readline()
		last_line = ""
		for line in f:
			line = line.lower()
			if (last_line != line) and (line.find("failed") == -1):
				last_line = line
				y = line.split('\t')
				print "UPDATE ud SET blogsearch = %d WHERE lemma = '%s';" % (int(y[1]), y[0].replace("\\", "\\\\").replace("'", "\\'").replace("\"", "\\\""))
				count += 1
print footer
