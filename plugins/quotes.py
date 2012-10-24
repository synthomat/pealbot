from random import shuffle
from plugin import Plugin

class Quotes(Plugin):
	def __init__(self):
		self.file_name = "quotes.txt"
		self.quotes = []
		try:
			self.quotes = open(self.file_name, 'r+').readlines()
		except:
			pass
	
	def get_random(self):
		from random import shuffle
		shuffle(self.quotes)
		return self.quotes[0]

	def add(self, text):
		self.quotes.append(text)

	def save(self):
		f = open(self.file_name, 'w')
		f.write("\n".join(self.quotes))
		f.close()