#!/usr/bin/env python

from pybot import BotBot


class PealBot(BotBot):
	def __init__(self, config):
		BotBot.__init__(self, config)

	def on_privmsg(self, params):
		text = params['text']

		if text.startswith('!'):
			self.handle_cmd(params)


	def handle_cmd(self, params):
		parts = params['text'].split()
		cmd = parts.pop(0)[1:]

		parts = ' '.join(parts)

		if cmd == "kill":
			self.quit()

		if cmd == "join" and parts:
			self.join(parts)

		if cmd == "part" and parts:
			self.part(parts)

	def on_cmd_kill(self, params):
		self.quit()

	def on_cmd_join(self, params):
		self.join()

	def on_cmd_part(self, params):
		self.part()


if __name__ == '__main__':
	config = {
		"server": ("irc.freenode.org", 6667),
		"autojoin": '#bsxlab',
		"autoload": [
			'quotes.Quotes'
		],

		"nick": "tastybot",
		"realname": "Cool Bot"
	}

	pb = PealBot(config)
	pb.start()