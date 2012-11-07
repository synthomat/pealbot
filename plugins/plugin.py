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

from lib.tools import Debug, lookup_hook
from lib.cyrusbus import Bus

class Plugin(object):
	def __init__(self, ctx):
		self.d = Debug("[Mod] " + self.__class__.__name__)
		self.ctx = ctx

	def subscribe(self, key, callback):
		self.ctx.bus.subscribe(key, callback)

	def ubsubscribe(self, key, callbask):
		self.ctx.bus.ubsubscribe(key, callback)

	def publish(self, key, *args, **kwargs):
		self.ctx.bus.publish(key, *args, **kwargs)


class CommandPlugin(Plugin):
	def __init__(self, ctx):
		Plugin.__init__(self, ctx)

		self.subscribe("irc.privmsg", self._on_privmsg)

	def _on_privmsg(self, msg):
		if msg.trail.startswith('!'):
			self._invoke(msg)

	def _invoke(self, msg):
		# distinguish between commands with and without parameters
		if ' ' in msg.trail:
			cmd, params = msg.trail.split(' ', 1)
		else:
			cmd, params = msg.trail, None

		# strip the ! away
		cmd = cmd.lstrip('!')

		meth = lookup_hook(self, cmd, prefix="on_cmd_")

		if meth:
			meth(params, msg)