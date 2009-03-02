from SOAPpy import SOAPProxy

class UrbanDictionary:
	def __init__(self, key):
		self.key = key
		self.server = SOAPProxy('http://api.urbandictionary.com/soap')

	def count_definitions(self, term):
		return self.server.count_definitions(self.key, term)

	def lookup(self, term):
		return self.server.lookup(self.key, term)
