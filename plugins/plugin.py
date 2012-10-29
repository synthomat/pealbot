# coding: utf-8

"""
Copyright 2012 Anton Zering <synth@lostprofile.de>

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

__all__ = ['Plugin', 'Command']

from lib.tools import Debug

class Plugin(object):
	# prevents the execution of the next's plugin hook
	LAST = 1

	def __init__(self, context):
		self.d = Debug("[Mod] " + self.__class__.__name__)
		
		self.context = context
		self.d.info("loaded...")

	def before_unload(self):
		pass

	def before_quit(self):
		pass

from lib.tools import lookup_hook

class CommandPlugin(Plugin):

	def on_privmsg(self, params):
		self.invoke(params)

	def invoke(self, parsed_msg):
		text = parsed_msg.get('text')

		if not text.startswith('!'):
			return

		if ' ' in text:
			cmd, params = text.split(' ', 1)
		else:
			cmd, params = text, None

		cmd = cmd.lstrip('!')

		meth = lookup_hook(self, cmd, lookup_table=None, prefix="on_cmd_")

		if meth:
			meth(params, parsed_msg)