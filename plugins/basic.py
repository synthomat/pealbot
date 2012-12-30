# coding: utf-8

"""
Copyright (c) 2012
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

import datetime
from plugin import Plugin

class Basic(Plugin):
	"""
	Essential plugin for the bot.
	It handles commands and autojoins.

	:author: Anton Zering <synth@lostprofile.de>
	:copyright: 2012, Anton Zering
	:license: Apache License, Version 2.0
	"""

	export = ['version', 'uptime', 'exports', 'plugins']

	def __init__(self, bot):
		Plugin.__init__(self, bot)

		self.start_time = datetime.datetime.now()
		self.subscribe("irc.rpl_endofmotd", self.autojoin)

	def autojoin(self, msg=None):
		"""RPL_ENDOFMOTD is used to auto join channels."""

		for chan in self.bot.config.AUTOJOIN:
			self.bot.join(chan)

	def on_cmd_uptime(self, msg, params):
		uptime = datetime.datetime.now() - self.start_time

		self.bot.msg(msg.params[0], "Uptime: " + str(uptime))

	def on_cmd_version(self, msg, params):
		self.bot.msg(msg.params[0], self.bot.__version__)

	def on_cmd_exports(self, msg, params):
		sender = msg.params[0]

		for p in self.bot.plugin_dispatcher.plugins:
			self.bot.msg(sender, "[%s]: %s" % (p.__class__.__name__, ', '.join(sorted(p.export))))

	def on_cmd_plugins(self, msg, params):
		sender = msg.params[0]
		names = ', '.join(sorted([p.__class__.__name__ for p in self.bot.plugin_dispatcher.plugins]))

		self.bot.msg(sender, "Plugins: %s" % names)