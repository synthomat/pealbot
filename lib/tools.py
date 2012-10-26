# coding: utf-8
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

import re
from termcolor import cprint

class Debug(object):
	"""
	Provides colorfull debugging messages.

	:requires: termcolor

	:author: Anton Zering <synth@lostprofile.de>

	:copyright: 2012, Anton Zering
	:license: Apache License, Version 2.0
	"""

	def __init__(self, prefix=""):
		"""
		Constructor

		A prefix text can be used which will be prepended in front of all debug messages.
		
		:param prefix: Prefix text
		"""		
		if prefix != "":
			self.prefix = ' %s:' % prefix
		else:
			self.prefix = prefix

	def info(self, text):
		"""
		Prints info message
		
		:param text: Info text to be printed
		"""
		cprint("--%s %s" % (self.prefix, text), 'green')

	def notice(self, text):
		"""
		Prints notice message
		
		:param text: Notice text to be printed
		"""
		cprint("--%s %s" % (self.prefix, text), 'cyan')

	def warn(self, text):
		"""
		Prints warn message
		
		:param text: Warning text to be printed
		"""
		cprint("--%s %s" % (self.prefix, text), 'yellow')

	def error(self, text):
		"""
		Prints info message
		
		:param text: Error text to be printed
		"""
		cprint("!!%s %s" % (self.prefix, text), 'red')


class IRCParser(object):
	"""
	Parses raw irc messages from the server

	:author: Anton Zering <synth@lostprofile.de>

	:copyright: 2012, Anton Zering
	:license: Apache License, Version 2.0
	"""

	def __init__(self):
		self.msg = None

		# compiled regular expression to parse irc messages		 
		self.rx = re.compile(r"(:((?P<nick>\w+)!~(?P<user>\w+)@)?(?P<host>\S*) )?(?P<cmd>\S+) (?P<dest>.+)?:(?P<text>.+)")

	def parse(self, raw_msg):
		try:
			# try to match regex
			self.msg = self.rx.match(raw_msg).groupdict()
		except:
			# match failed - reset msg
			self.msg = None
			return None

		# lowercase uppercase irc commands
		self.msg['cmd'] = self.msg['cmd'].lower()

		# split destination part into a python list
		if self.msg['dest']:
			self.msg['dest'] = self.msg['dest'].split()

		return self.msg

	def get(self, key, default=None):
		try:
			return self.msg[key]
		except:
			return default

def lookup_hook(context, name, prefix="on_", lookup_table=None):
	"""
	Lookup chain:

	1. member method with prefix (i.e. on_join, on_351)
	2. method within lookup table
	3. raise exception

	:param context: Blablubb
	"""	
	
	name = prefix + name
	method = None
	if name in dir(context):
		method = getattr(context, name)
	elif name.isdigit():
		pass

	return method