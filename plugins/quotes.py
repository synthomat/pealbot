"""
Copyright (c) 2012 

Anton Zering <synth@lostprofile.de>
Julian Held <nemesis@creative-heads.org>

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
from plugin import CommandPlugin
from random import shuffle
class Quotes(CommandPlugin):
	
	def __init__(self, context):
		CommandPlugin.__init__(self, context)
		self.file_name = "quotes.txt"
		self.quotes = []
		try:
			self.quotes = open(self.file_name, 'r+').readlines()
		except:
			pass
	
	def get_random(self):
		if self.quotes:
			return "No quotes available!"
		else:
			shuffle(self.quotes)
			return self.quotes[0]

	def add(self, text):
		self.quotes.append(text)

	def save(self):
		f = open(self.file_name, 'w')
		f.write("\n".join(self.quotes))
		f.close()

	def on_cmd_add(self, p, msg):
		chan = msg.targets[0]
		self.add(p)
		self.context.msg(chan, "Added quote: %s!" % p)

	def on_cmd_q(self, p, msg):
		chan = msg.targets[0]
		quote = self.get_random()
		self.context.msg(chan, "%s" % quote)
	
	def before_unload(self):
		self.save()