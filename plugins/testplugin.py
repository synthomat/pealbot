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

from plugin import CommandPlugin
import datetime
class TestPlugin(CommandPlugin):
	def __init__(self, context):
		CommandPlugin.__init__(self, context)

	def on_cmd_say(self, p, params):
		chan = params['dest'][0]
		nick = params['nick']
		self.context.msg(chan, "%s" % p)

	def on_cmd_kill(self, p, params):
		self.context.quit()

	def on_cmd_join(self, p, params):
		self.context.join(p)

	def on_cmd_part(self, p, params):
		chan = params['dest'][0]
		self.context.part(chan)

	def on_cmd_now(self, p, params):
		chan = params['dest'][0]

		self.context.msg(chan, datetime.datetime.now())
