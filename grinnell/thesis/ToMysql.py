#!/usr/bin/python
import os

print "create table if not exists ud (id int auto_increment primary key, lemma varchar(100), defs int(10), up int, down int);"
print "TRUNCATE TABLE ud;"

header = "INSERT INTO ud (lemma, defs, up, down) VALUES"
footer = ";"

count = 0
for file in os.listdir('data/'):
	if file.startswith('stats-'):
		f = open('data/' + file, 'r')
		f.readline()
		last_line = ""
		for line in f:
			line = line.lower()
			if (last_line != line) and (line.find("failed") == -1):
				if count % 1000 == 0:
					if count != 0: print footer
					print header
				else:
					print ", ", 
				last_line = line
				y = line.split('\t')
				print "('%s', %s, %s, %s)" % (y[0].replace("\\", "\\\\").replace("'", "\\'").replace("\"", "\\\""), y[1], y[2], y[3])
				count += 1
print footer
