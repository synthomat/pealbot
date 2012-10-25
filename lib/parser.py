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

class IRCParser(object):
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