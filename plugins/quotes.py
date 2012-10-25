"""
Copyright 2012
	Anton Zering <synth@lostprofile.de>

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

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