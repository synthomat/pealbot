from plugin import Plugin

class Basic(Plugin):

	def __init__(self):
		Plugin.__init__(self)

	def on_privmsg(self, params):
		text = params['text']

		if text.startswith('!') and text == "!kill":
			self.c.quit()