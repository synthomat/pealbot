#!/usr/bin/env python
# coding: utf-8

"""
Copyright (c) 2012 Anton Zering <synth@lostprofile.de>

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

import os.path
from lib.pybot import BotBot
from lib.plugindispatcher import PluginDispatcher
from lib.tools import Debug

class PealBot(BotBot):
	"""
	:author: Anton Zering <synth@lostprofile.de>
	:author: Jules Held <nemesis@creative-heads.org>
	:copyright: 2012, Anton Zering
	:license: Apache License, Version 2.0
	"""

	def __init__(self, config):
		BotBot.__init__(self, config.HOST, config.IDENTITY['nick'], config.IDENTITY['realname'])
		self.config = config
		self.d = Debug()

		# initialize PluginDispatcher and autoload modules
		self.plugin_dispatcher = PluginDispatcher(self, config.PATHS['plugins'])
		self.plugin_dispatcher.load_plugins(config.PLUGINS)

	def handle_irc(self, msg):
		# handle "built in" event hooks
		BotBot.handle_irc(self, msg)

		# handle plugin event hooks
		self.plugin_dispatcher.handle_irc(msg)

	def exit(self, exit_code=0):
		"""Invokes the before_unload hook of all loaded plugins before the module gets unloaded."""
		# invoke system hook
		self.plugin_dispatcher.invoke_all("before_unload")
		BotBot.exit(self, exit_code)

	def quit(self, quit_reason=''):
		"""Invokes the before_quit hook of all loaded plugins before the QUIT message is sent to the server."""
		# invoke system hook
		self.plugin_dispatcher.invoke_all("before_quit")
		BotBot.quit(self, quit_reason)


if __name__ == '__main__':
	try:
		import config
	except:
		print "Configuration could not be found."
		sys.exit(1)

	pb = PealBot(config)
	pb.start()
