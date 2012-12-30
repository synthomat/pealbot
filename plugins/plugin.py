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

__all__ = ['Plugin', 'CommandPlugin']

from lib.tools import Debug
from lib.cyrusbus import Bus

class Plugin(object):
	export = []
	key = '!'

	def __init__(self, bot):
		self.d = Debug("[Mod] " + self.__class__.__name__)
		self.bot = bot
		self.subscribe("irc.privmsg", self.invoke_cmd)

		self.export = [e.lower() for e in self.export]

	def invoke_cmd(self, msg):
		if not msg.text.startswith(self.key):
			return

		cmd, _, params = msg.text[1:].partition(' ')
		cmd = cmd.lower()

		if not cmd in self.export:
			return
		try:
			method_name = "on_cmd_" + cmd
			method = getattr(self, method_name)
			method(msg, params)
		except Exception as e:
			print e
			return

	def subscribe(self, key, callback):
		self.bot.bus.subscribe(key, callback)

	def ubsubscribe(self, key, callbask):
		self.bot.bus.ubsubscribe(key, callbask)

	def publish(self, key, *args, **kwargs):
		self.bot.bus.publish(key, *args, **kwargs)