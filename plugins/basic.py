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

from plugin import Plugin

class Basic(Plugin):
	def __init__(self, context):
		Plugin.__init__(self, context)

	def on_privmsg(self, params):
		text = params['text']

		if text.startswith('!') and text == "!kill":
			self.context.quit()

	def on_rpl_endofmotd(self, params):
		# autojoin channels
		for chan in self.context.config.AUTOJOIN:
			self.context.join(chan)

	def auth(self, password):
		self.context.msg('nickserv', 'identify %s %s' % (self.nickname, password))