#!/usr/bin/env python
import os.path
from lib.pybot import BotBot
from lib.plugindispatcher import PluginDispatcher

class PealBot(BotBot):
	def __init__(self, config):
		BotBot.__init__(self, config)
		
		self.plugin_dispatcher = None
		self.init_plugins()

	def init_plugins(self):
		script_dir = os.path.dirname(__file__)
		plugin_dir = os.path.join(script_dir, self.config['plugindir'])

		self.plugin_dispatcher = PluginDispatcher(self, plugin_dir)
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
			'quotes.Quotes',
		],

		"nick": "jxBot",
		"realname": "Cool Bot",
		"password": "XXXXXXX"
	}

	pb = PealBot(config)
	pb.start()
