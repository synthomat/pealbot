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

import importlib
import sys
from tools import Debug, lookup_hook
from pybot import codes

class PluginDispatcher(object):
	"""
	PluginDispatcher loads modules and handles event hooks in them

	:author: Anton Zering <synth@lostprofile.de>
	:copyright: 2012, Anton Zering
	:license: Apache License, Version 2.0
	"""
	def __init__(self, context, plugin_dir="plugins"):
		self.d = Debug()
		
		# apply plugin dir to PATH
		sys.path.append(plugin_dir)

		# context object
		self.context = context
		self.plugins = []

	def load_plugins(self, path_list):
		self.d.info("Loading modules...")
		for path in path_list:
			cls = self.get_class_by_path(path)
			if cls:
				self.plugins.append(cls(self.context))

	def get_class_by_path(self, path):
		"""
		Returns a class object by path

		:param path: Path to the plugin in module notation: module.module.PluginClass
		:returns: Class object
		"""
		# separate class from modul name
		mod_name, cls_name = path.rsplit('.', 1)

		try:
			cls = __import__(mod_name).__dict__[cls_name]
		except Exception, e:
			# plugin could not be loaded due to lookup error or syntax errors.
			self.d.warn("!! FAILED loading module %s (%s)" % (path, e))
			return None

		return cls

	def invoke_all(self, method_name):
		"""
		Invokes a given method by it's name in all loaded plugins

		:param method_name: Method name to be called
		"""
		for plugin in self.plugins:
			if method_name in dir(plugin):
				m = getattr(plugin, method_name)
				m()

	def handle_irc(self, msg):
		"""
		Invokes looked up method in all loaded modules based on the parsed irc message

		:param msg: Parsed irc message (IRCParser)
		"""
		for plugin in self.plugins:
			method = lookup_hook(plugin, msg.get('cmd'), codes)

			if method:
				ret = method(msg)
				
				if ret == plugin.LAST:
					break