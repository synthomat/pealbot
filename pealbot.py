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
	def __init__(self, config):
		BotBot.__init__(self, config['server'], config['nick'], config['realname'])
		self.config = config
		self.d = Debug()

		# initialize PluginDispatcher and autoload modules
		self.plugin_dispatcher = PluginDispatcher(self, self.config['plugindir'])
		self.plugin_dispatcher.load_plugins(self.config['autoload'])

	def on_privmsg(self, params):
		text = params['text']

	def invoke_hook(self, method, msg_parts):
		BotBot.invoke_hook(self, method, msg_parts)
		self.plugin_dispatcher.invoke_hook(method, msg_parts)

if __name__ == '__main__':
	config = {
		"server": ("irc.freenode.org", 6667),
		"autojoin": '#bsxlab',
		"plugindir": "plugins",
		"autoload": [
			'basic.Basic',
			'quotes.Quotesa',
		],

		"nick": "jxBoa",
		"realname": "Cool Bot",
		"password": "XXXXXXX"
	}

	pb = PealBot(config)
	pb.start()
