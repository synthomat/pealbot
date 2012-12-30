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

import threading
import re

class Reminder(Plugin):
	export = ['remind']

	def __init__(self, bot):
		Plugin.__init__(self, bot)

	def remember(self, chan, nick, text):
		self.bot.msg(chan, "%s: [TIMER]: %s" % (nick, text))

	def on_cmd_remind(self, msg, params):
		chan = msg.params[0]
		nick = msg.nick

		try:
			time, _, text = msg.text.partition(' ')
			m = re.match(r"(\d+)(.?)", params)

			time, unit = 0, 'm'

			if not m: return

			time, unit = m.groups()

			seconds = float(time)

			if unit == 's':
				pass
			elif unit == ('' or 'm'):
				seconds = seconds * 60
			elif unit == 'h':
				seconds = seconds * 60 * 60

			timer = threading.Timer(seconds, self.remember, [chan, nick, text])
			timer.start()
			self.bot.msg(chan, "%s: timer set for %s%s." % (nick, time, unit))
		except:
			self.bot.msg(chan, "[Reminder] Usage: NUMBER[h|m|s] LONG DESCRIPTION TEXT")