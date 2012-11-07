#!/usr/bin/env python
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

import os.path
import re
import socket
import sys

from lib.cyrusbus import Bus
from lib.tools import lookup_hook, irc_codes


_rfc1459_message = re.compile(r"(:((?P<nick>\S+)!~(?P<user>\S+)@)?(?P<host>\S+) )?(?P<cmd>\w+) (?P<params>.+)")

class IRCMessage(object):
	def __init__(self, nick, user, host, cmd, params):
		self.nick = nick
		self.user = user
		self.host = host
		self.cmd = cmd.lower()
		self.params = params
		
		(self.targets, _, self.trail) = params.partition(':')
		self.targets = self.targets.strip().split()

	def __repr__(self):
		return "<IRCMessage nick=%s user=%s host=%s cmd=%s targets=%s trail='%s'" \
				% (self.nick, self.user, self.host, self.cmd, self.targets, self.trail)

	@staticmethod
	def parse(raw_msg, throw_exception=False):
		if type(raw_msg) == dict:
			return self(**raw_msg)
		elif type(raw_msg) == str:
			try:
				parsed = re.compile(_rfc1459_message).match(raw_msg)
				return IRCMessage(**parsed.groupdict())
			except Exception, e:
				if throw_exception:
					raise Exception("IRC message could not be parsed", e)
				return

class PluginDispatcher(object):
	"""
	PluginDispatcher loads modules and handles event hooks in them

	:author: Anton Zering <synth@lostprofile.de>
	:copyright: 2012, Anton Zering
	:license: Apache License, Version 2.0
	"""
	def __init__(self, ctx, plugin_dir="plugins"):
		# apply plugin dir to PATH
		sys.path.append(plugin_dir)

		# context object
		self.ctx = ctx
		self.plugins = []

	def load_plugins(self, path_list):
		for path in path_list:
			cls = self.get_class_by_path(path)
			if cls:
				try:
					self.plugins.append(cls(self.ctx))
					self.ctx.debug("Plugin: %s loaded" % path)
				except:
					self.ctx.debug("Plugin: could not load " + path)

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
			return None

		return cls

	def handle_irc(self, msg):
		"""
		Invokes looked up method in all loaded modules based on the parsed irc message

		:param msg: Parsed irc message (IRCParser)
		"""
		
		cmd = msg.cmd

		if cmd in irc_codes:
			cmd = irc_codes[cmd]

		self.ctx.bus.publish("irc."+cmd, msg)


class PealBot(object):
	"""
	:author: Anton Zering <synth@lostprofile.de>
	:author: Jules Held <nemesis@creative-heads.org>
	:copyright: 2012, Anton Zering
	:license: Apache License, Version 2.0
	"""

	def __init__(self, config):
		""" 
		Constructor for the bot

		:param host: The server address as tuple of (HOST, PORT)
		:param nick_name: Nickname for the bot.
		:param real_name: Real name of the bot. It not provided, the nick is taken as real name.
		"""
		self.config = config

		
		self.host = config.HOST
		self.nick_name = config.IDENTITY['nick']
		self.real_name = config.IDENTITY['realname']

		if self.real_name:
			self.real_name = self.real_name
		else:
			self.real_name = self.nick_name

		self.channels = {}
		self.bus = Bus()

		# initialize PluginDispatcher and autoload modules
		self.plugin_dispatcher = PluginDispatcher(self, config.PATHS['plugins'])
		self.plugin_dispatcher.load_plugins(config.PLUGINS)

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


	def debug(self, text):
		print "-- " + text

	def connect(self, host=None):
		"""
		Connects to the server

		:param host: The server address as tuple of (HOST, PORT).
		"""

		if not host:
			host = self.host

		self.debug("Connecting to " + str(host))

		# connect to server socket
		self.sock.connect(self.host)

		# set default nick name
		self.nick(self.nick_name)

		# set default user and real name
		self.send("USER %s 0 0 :%s" % (self.nick_name, self.real_name))

	def disconnect(self):
		"""Disconnects from the server if already connected."""

		if not self.sock:
			return

		self.debug("Disconnecting from " + str(self.host))
		self.sock.close()

	def send(self, msg):
		"""
		Sends raw messages to the server.

		:param msg: Message to be sent.

		:return: success of the send operation
		"""

		self.debug("<< " + msg)
		return self.sock.sendall(msg + "\r\n")

	def quit(self, quit_reason=""):
		"""
		Sends a QUIT command to the server. Then disconnects.

		:param quit_msg: Quit message.
		"""

		self.bus.publish("plugins.before_quit")

		self.send('QUIT %s' % quit_reason)
		self.disconnect()

	def join(self, channels):
		"""
		Sends a JOIN message to the server to joins one or multiple channels

		:param channels: One or more channels separated by whitespaces.
		"""

		return self.send('JOIN %s' % channels)

	def part(self, channels, part_reason=None):
		"""
		Sends the PART message to the searver to leave one or multiple channels

		:param channels: One or more channels separated by whitespaces.
		:param part_msg: Part message to appear in the channel
		"""

		return self.send('PART %s :%s' % (channels, part_reason))

	def nick(self, new_nick):
		"""
		Sends the NICK message to the server to try a nickname change of the bot

		:param new_nick: The new nick
		"""

		return self.send("NICK %s" % new_nick)

	def notice(self, target, text):
		"""
		Sends a NOTICE message to a reciever

		:param target: Reciever of the message
		:param msg: Message to be sent
		"""

		return self.send("NOTICE %s :%s" % (target, text))

	def msg(self, target, text):
		"""
		Sends a PRIVMSG message to a channel or another client

		:param target: Reciever of the message. Channel or a nick name.
		:param msg: Message to be sent
		"""
		return self.send("PRIVMSG %s :%s" % (target, text))

	def exit(self, exit_code=0):
		self.bus.publish("plugins.before_unload")
		sys.exit(exit_code)

	def start(self):
		# connect to server
		self.connect()
		
		# TODO: move to plugin!
		# Authenticate at Nickserv:
		# self.auth(self.config['password'])

		while True:
			try:
				recv = self.sock.recv(2048)
				# print recv
			except:
				self.exit(0)

			for line in recv.split("\r\n"):

				# ignore empty lines
				if not line: continue

				# handle irc commands
				msg = IRCMessage.parse(line)

				if msg:
					# handle PING message
					if msg.cmd == 'ping':
						self.send("PONG :%s" % msg.trail)
					else:
						self.handle_irc(msg)

	def handle_irc(self, msg):
		method = lookup_hook(self, msg.cmd)
		self.plugin_dispatcher.handle_irc(msg)

		if method:
			return method(msg)


if __name__ == '__main__':
	try:
		import config
	except:
		print "Configuration could not be found."
		sys.exit(1)

	pb = PealBot(config)
	pb.start()