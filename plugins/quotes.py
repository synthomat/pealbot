from random import shuffle

class Quotes(Plugin):
	def __init__(self, file_name):
		self.file_name = file_name
		self.quotes = []
		try:
			self.quotes = open(file_name, 'r+').readlines()
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