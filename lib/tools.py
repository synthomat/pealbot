# coding: utf-8
"""
Copyright 2012
	Anton Zering <synth@lostprofile.de>

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

from termcolor import cprint

class Debug(object):
	def __init__(self, prefix=""):
		self.prefix = prefix

		if prefix != "":
			self.prefix = ' %s:' % prefix

	def info(self, text):
		cprint("--%s %s" % (self.prefix, text), 'green')

	def notice(self, text):
		cprint("--%s %s" % (self.prefix, text), 'cyan')

	def warn(self, text):
		cprint("--%s %s" % (self.prefix, text), 'yellow')

	def error(self, text):
		cprint("!!%s %s" % (self.prefix, text), 'red')


def lookup_hook(context, name, prefix="on_", lookup_table=None):
	""" Lookup chain:
		1. member method with prefix (i.e. on_join, on_351)
		2. method within lookup table
		3. raise exception
	"""	
	
	name = prefix + name
	method = None
	if name in dir(context):
		method = getattr(context, name)
	elif name.isdigit():
		pass

	return method