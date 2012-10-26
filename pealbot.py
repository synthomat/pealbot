#!/usr/bin/env python
# coding: utf-8

"""
Copyright 2012
   Anton Zering <synth@lostprofile.de>
   Jules Held <nemesis@creative-heads.org>

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

	def invoke_hook(self, method, msg_parts):
		BotBot.invoke_hook(self, method, msg_parts)
		self.plugin_dispatcher.invoke_hook(method, msg_parts)

if __name__ == '__main__':
	import config

	pb = PealBot(config)
	pb.start()
