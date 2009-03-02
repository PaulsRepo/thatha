from UrbanDictionaryAPI import UrbanDictionary

ud = UrbanDictionary('a237993550175803efbf9530ff4de2bc')
file = open("data/ud20090220-popular-01.txt")
for line in file:
	line = line.strip()
	try:
		count = ud.count_definitions(line)
		print "%s\t%d" % (line, count)
	except Exception:
		pass
