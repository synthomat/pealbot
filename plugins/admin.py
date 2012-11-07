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

class Admin(CommandPlugin):	
	def __init__(self, ctx):
		CommandPlugin.__init__(self, ctx)

	def on_cmd_kill(self, p, msg):
		self.ctx.quit()

	def on_cmd_join(self, p, msg):
		self.ctx.join(p)

	def on_cmd_part(self, p, msg):
		chan = msg.targets[0]
		self.ctx.part(chan)