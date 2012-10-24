from random import shuffle
from plugin import Plugin

class Quotes(Plugin):
	def __init__(self):
		Plugin.__init__(self)

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
		print "Adding %s" % text
		self.quotes.append(text)

	def save(self):
		f = open(self.file_name, 'w')
		f.write("\n".join(self.quotes))
		f.close()

	def on_privmsg(self, params):
		text = params['text']

		if not text.startswith('!'):
			return

		print "Q: Command!"

		try:
			if ' ' in text:
				cmd, par = text.split(' ', 1)
			else:
				cmd, par = text, None
			
			cmd = cmd[1:]

			if cmd == "add":
				self.add(par)
				return

			if cmd == "q":
				self.c.msg(params['dest'], self.get_random())
				return

		except:
			return