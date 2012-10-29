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
__all__ = ['Debug', 'lookup_hook']

from termcolor import cprint

class Debug(object):
	"""
	Provides colorfull debugging messages.

	:requires: termcolor

	:author: Anton Zering <synth@lostprofile.de>

	:copyright: 2012, Anton Zering
	:license: Apache License, Version 2.0
	"""

	def __init__(self, prefix=""):
		"""
		Constructor

		A prefix text can be used which will be prepended in front of all debug messages.
		
		:param prefix: Prefix text
		"""		
		if prefix != "":
			self.prefix = ' %s:' % prefix
		else:
			self.prefix = prefix

	def info(self, text):
		"""
		Prints info message
		
		:param text: Info text to be printed
		"""
		cprint("--%s %s" % (self.prefix, text), 'green')

	def notice(self, text):
		"""
		Prints notice message
		
		:param text: Notice text to be printed
		"""
		cprint("--%s %s" % (self.prefix, text), 'cyan')

	def warn(self, text):
		"""
		Prints warn message
		
		:param text: Warning text to be printed
		"""
		cprint("--%s %s" % (self.prefix, text), 'yellow')

	def error(self, text):
		"""
		Prints info message
		
		:param text: Error text to be printed
		"""
		cprint("!!%s %s" % (self.prefix, text), 'red')

def lookup_hook(context, name, lookup_table=None, prefix="on_"):
	"""
	Lookup chain:

	1. return member method with prefix (i.e. on_join, on_351)
	2. return method within lookup table (resolve method_name by numeric command)
	3. return none

	:param context: object to be instrospected
	:param name: method name to find
	:param lookup_table: lookup table as dict
	:param prefix: search with prefix in the method name

	:return: method reference
	"""

	method = None
	method_name = prefix + str(name)

	# hook name exists in context?
	if method_name in dir(context):
		return getattr(context, method_name)

	# lookup_table provided? name is digit and can be looked up?
	elif lookup_table and str(name).isdigit() and int(name) in lookup_table:
		name = int(name)

		# resolve code to hook name
		method_name = prefix + lookup_table[name]

		# hook name exists in context?
		if method_name in dir(context):
			return getattr(context, prefix + lookup_table[name])

	return None