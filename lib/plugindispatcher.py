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

import sys
from tools import Debug

class PluginDispatcher(object):
	def __init__(self, context, plugin_dir):
		# apply plugin dir to PATH
		sys.path.append(plugin_dir)

		self.d = Debug()

		self.context = context
		self.plugins = []

	def load_plugins(self, path_list):
		self.d.info("Loading modules...")
		for path in path_list:
			cls = self.get_class_by_path(path)
			if cls:
				setattr(cls, 'c', self.context)
				self.plugins.append(cls())

	def get_class_by_path(self, path):
		try:
			module, cls_name = path.rsplit('.', 1)
			classes = __import__(module, globals(), locals(), [cls_name], -1)
			cls = classes.__dict__[cls_name]
		except:
			self.d.warn("!! FAILED loading module %s" % path)
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
