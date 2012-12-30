# coding: utf-8

"""
Copyright (c) 2012 

Anton Zering <synth@lostprofile.de>
Julian Held <nemesis@creative-heads.org>

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

from plugin import Plugin

try:
	from lib.pyaspell import Aspell
	aspell = Aspell([('lang', 'de'), ('ignore-case', 'true')])
except:
	aspell = None


class Aspell(Plugin):
	export = ['spell']

	def __init__(self, bot):
		Plugin.__init__(self, bot)

		# we can't use spell on windows machines :(
		if aspell:
			self.aspell = aspell
		else:
			self.on_cmd_spell = lambda msg, p: self.bot.msg(msg.params[0], "[Spell]: disabled")

	def on_cmd_spell(self, msg, params):
		chan = msg.params[0]

		word, _, _ = params.partition(' ')

		try:
			if self.aspell.check(word):
				self.bot.msg(chan, "[Spell]: [%s] - OK." % word)
			else:
				words = ', '.join(self.aspell.suggest(word))
				if len(words):
					self.bot.msg(chan, "[Spell]: [%s] - suggestions: [%s]" % (word, words))
				else:
					self.bot.msg(chan, "[Spell]: [%s] - no suggestions found." % word)
		except:
			self.bot.msg(chan, "[Spell]: [%s] could not check." % word)
