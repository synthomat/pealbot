import sys

class PluginDispatcher(object):
	def __init__(self, context, plugin_dir):
		self.plugin_dir = plugin_dir
		sys.path.append(plugin_dir)
		self.plugins = []
		self.context = context


	def load_plugins(self, path_list):
		for path in path_list:
			print "-- loading %s" % path
			cls = self.get_class_by_path(path)
			setattr(cls, 'c', self.context)
			self.add_plugin(cls())

	def add_plugin(self, plugin_class):
		self.plugins.append(plugin_class)

	def get_class_by_path(self, path):
		try:
			module, cls_name = path.rsplit('.', 1)
			classes = __import__(module, globals(), locals(), [cls_name], -1)
			cls = classes.__dict__[cls_name]
		except:
			print "FAILED importing module %s" % path
			return

		return cls

	def invoke_hook(self, method, msg_parts):
		for plugin in self.plugins:
			if method in dir(plugin):
				print "-- %s found in %s" % (method, plugin)
				hook = getattr(plugin, method)
				ret = hook(msg_parts)

				if ret == plugin.LAST:
					break
