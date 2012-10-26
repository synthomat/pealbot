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

import importlib
import sys
from tools import Debug

class PluginDispatcher(object):
	def __init__(self, context, plugin_dir="plugins"):
		self.d = Debug()
		
		# apply plugin dir to PATH
		sys.path.append(plugin_dir)

		self.context = context
		self.plugins = []

	def load_plugins(self, path_list):
		self.d.info("Loading modules...")
		for path in path_list:
			cls = self.get_class_by_path(path)
			if cls:
				self.plugins.append(cls(self.context))

	def get_class_by_path(self, path):
		mod_name, cls_name = path.rsplit('.', 1)

		try:
			cls = __import__(mod_name).__dict__[cls_name]
		except Exception, e:
			self.d.warn("!! FAILED loading module %s (%s)" % (path, e))
			return None

		return cls

	def invoke_hook(self, method, msg_parts):
		for plugin in self.plugins:
			if method in dir(plugin):
				print "-- %s found in %s" % (method, plugin)
				hook = getattr(plugin, method)
				ret = hook(msg_parts)

				if ret == plugin.LAST:
					break
