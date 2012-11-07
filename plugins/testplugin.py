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

from plugin import CommandPlugin
import datetime
class TestPlugin(CommandPlugin):	
	def __init__(self, ctx):
		CommandPlugin.__init__(self, ctx)

		self.starttime = datetime.datetime.now()
	
	def calc_onlinetime(self):
		timenow = datetime.datetime.now()
		onlinetime = timenow - self.starttime
		return onlinetime
	
	def on_cmd_online(self, p, msg):
		chan = msg.targets[0]
		self.ctx.msg(chan, self.calc_onlinetime())
	
	def on_cmd_status(self, p, msg):
		chan = msg.targets[0]
		self.ctx.msg(chan,  "Online for: %s" % self.calc_onlinetime())

	def on_cmd_say(self, p, msg):
		chan = msg.targets[0]
		nick = msg.nick
		self.ctx.msg(chan, "%s" % p)

	def on_cmd_now(self, p, msg):
		chan = msg.targets[0]
		self.ctx.msg(chan, datetime.datetime.now())
