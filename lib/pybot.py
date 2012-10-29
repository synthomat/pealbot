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

import re
import socket
import sys

from tools import Debug, IRCParser, lookup_hook

codes = {
	##
	## error codes
	##
	401: 'err_nosuchnick',		# <nickname> :no such nick/channel
	402: 'err_nosuchserver',	# <server name> :no such server
	403: 'err_nosuchchannel',	# <channel name> :no such channel
	404: 'err_cannotsendtochan',# <channel name> :cannot send to channel
	405: 'err_toomanychannels',	# <channel name> :you have joined too many channels
	406: 'err_wasnosuchnick',	# <nickname> :there was no such nickname
	407: 'err_toomanytargets',	# <target> :duplicate recipients. no message delivered
	409: 'err_noorigin',		# :no origin specified
	411: 'err_norecipient',		# :no recipient given (<command>)
	412: 'err_notexttosend',	# :no text to send
	413: 'err_notoplevel',		# <mask> :no toplevel domain specified
	414: 'err_wildtoplevel',	# <mask> :wildcard in toplevel domain
	421: 'err_unknowncommand',	# <command> :unknown command
	422: 'err_nomotd',			# :motd file is missing
	423: 'err_noadmininfo',		# <server> :no administrative info available
	424: 'err_fileerror',		# :file error doing <file op> on <file>
	431: 'err_nonicknamegiven',	# :no nickname given
	432: 'err_erroneusnickname',# <nick> :erroneus nickname
	433: 'err_nicknameinuse',	# <nick> :nickname is already in use
	436: 'err_nickcollision',	# <nick> :nickname collision kill
	441: 'err_usernotinchannel',# <nick> <channel> :they aren't on that channel
	442: 'err_notonchannel',	# <channel> :you're not on that channel
	443: 'err_useronchannel',	# <user> <channel> :is already on channel
	444: 'err_nologin',			# <user> :user not logged in
	445: 'err_summondisabled',	# :summon has been disabled
	446: 'err_usersdisabled',	# :users has been disabled
	451: 'err_notregistered',	# :you have not registered
	461: 'err_needmoreparams',	# <command> :not enough parameters
	462: 'err_alreadyregistred',# :you may not reregister
	463: 'err_nopermforhost',	# :your host isn't among the privileged
	464: 'err_passwdmismatch',	# :password incorrect
	465: 'err_yourebannedcreep',# :you are banned from this server
	467: 'err_keyset',			# <channel> :channel key already set
	471: 'err_channelisfull',	# <channel> :cannot join channel (+l)
	472: 'err_unknownmode',		# <char> :is unknown mode char to me
	473: 'err_inviteonlychan',	# <channel> :cannot join channel (+i)
	474: 'err_bannedfromchan',	# <channel> :cannot join channel (+b)
	475: 'err_badchannelkey',	# <channel> :cannot join channel (+k)
	481: 'err_noprivileges',	# :permission denied- you're not an irc operator
	482: 'err_chanoprivsneeded',# <channel> :you're not channel operator
	483: 'err_cantkillserver',	# :you cant kill a server!
	491: 'err_nooperhost',		# :no o-lines for your host
	501: 'err_umodeunknownflag',# :unknown mode flag
	502: 'err_usersdontmatch',	# :cant change mode for other users

	##
	## command responses
	##
	300: 'rpl_none',			# dummy reply number. not used.
	302: 'rpl_userhost',		# :[<reply>{<space><reply>}] // <reply> ::= <nick>['*'] '=' <'+'|'-'><hostname>
	303: 'rpl_ison',			# :[<nick> {<space><nick>}]
	301: 'rpl_away',			# <nick> :<away message>
	305: 'rpl_unaway',			# :you are no longer marked as being away
	306: 'rpl_nowaway',			# :you have been marked as being away
	311: 'rpl_whoisuser',		# <nick> <user> <host> * :<real name>
	312: 'rpl_whoisserver',		# <nick> <server> :<server info>
	313: 'rpl_whoisoperator',	# <nick> :is an irc operator
	317: 'rpl_whoisidle',		# <nick> <integer> :seconds idle
	318: 'rpl_endofwhois',		# <nick> :end of /whois list
	319: 'rpl_whoischannels',	# <nick> :{[@|+]<channel><space>}
	314: 'rpl_whowasuser',		# <nick> <user> <host> * :<real name>
	369: 'rpl_endofwhowas',		# <nick> :end of whowas
	321: 'rpl_liststart',		# channel :users name
	322: 'rpl_list',			# <channel> <# visible> :<topic>
	323: 'rpl_listend',			# :end of /list
	324: 'rpl_channelmodeis',	# <channel> <mode> <mode params>
	331: 'rpl_notopic',			# <channel> :no topic is set
	332: 'rpl_topic',			# <channel> :<topic>
	341: 'rpl_inviting',		# <channel> <nick>
	342: 'rpl_summoning',		# <user> :summoning user to irc
	351: 'rpl_version',			# <version>.<debuglevel> <server> :<comments>
	352: 'rpl_whoreply',		# <channel> <user> <host> <server> <nick> <h|g>[*][@|+] :<hopcount> <real name>
	315: 'rpl_endofwho',		# <name> :end of /who list
	353: 'rpl_namreply',		# <channel> :[[@|+]<nick> [[@|+]<nick> [...]]]
	366: 'rpl_endofnames',		# <channel> :end of /names list
	364: 'rpl_links',			# <mask> <server> :<hopcount> <server info>
	365: 'rpl_endoflinks',		# <mask> :end of /links list
	367: 'rpl_banlist',			# <channel> <banid>
	368: 'rpl_endofbanlist',	# <channel> :end of channel ban list
	371: 'rpl_info',			# :<string>
	374: 'rpl_endofinfo',		# :end of /info list
	375: 'rpl_motdstart',		# :- <server> message of the day -
	372: 'rpl_motd',			# :- <text>
	376: 'rpl_endofmotd',		# :end of /motd command
	381: 'rpl_youreoper',		# :you are now an irc operator
	382: 'rpl_rehashing',		# <config file> :rehashing
	391: 'rpl_time',			# <server> :<string showing server's local time>
	392: 'rpl_usersstart',		# :userid terminal host
	393: 'rpl_users',			# :%-8s %-9s %-8s
	394: 'rpl_endofusers',		# :end of users
	395: 'rpl_nousers',			# :nobody logged in
	200: 'rpl_tracelink',		# link <version & debug level> <destination> <next server>
	201: 'rpl_traceconnecting',	# try. <class> <server>
	202: 'rpl_tracehandshake',	# h.s. <class> <server>
	203: 'rpl_traceunknown',	# ???? <class> [<client ip address in dot form>]
	204: 'rpl_traceoperator',	# oper <class> <nick>
	205: 'rpl_traceuser',		# user <class> <nick>
	206: 'rpl_traceserver',		# serv <class> <int>s <int>c <server> <nick!user|*!*>@<host|server>
	208: 'rpl_tracenewtype',	# <newtype> 0 <client name>
	261: 'rpl_tracelog',		# file <logfile> <debug level>
	211: 'rpl_statslinkinfo',	# <linkname> <sendq> <sent messages> <sent bytes> <received messages> <received bytes> <time open>
	212: 'rpl_statscommands',	# <command> <count>
	213: 'rpl_statscline',		# "c <host> * <name> <port> <class>
	214: 'rpl_statsnline',		# n <host> * <name> <port> <class>
	215: 'rpl_statsiline',		# i <host> * <host> <port> <class>
	216: 'rpl_statskline',		# k <host> * <username> <port> <class>
	218: 'rpl_statsyline',		# y <class> <ping frequency> <connect frequency> <max sendq>
	219: 'rpl_endofstats',		# <stats letter> :end of /stats report
	241: 'rpl_statslline',		# l <hostmask> * <servername> <maxdepth>
	242: 'rpl_statsuptime',		# :server up %d days %d:%02d:%02d
	243: 'rpl_statsoline',		# o <hostmask> * <name>
	244: 'rpl_statshline',		# h <hostmask> * <servername>
	221: 'rpl_umodeis',			# <user mode string>
	251: 'rpl_luserclient',		# :there are <integer> users and <integer> invisible on <integer> servers
	252: 'rpl_luserop',			# <integer> :operator(s) online
	253: 'rpl_luserunknown',	# <integer> :unknown connection(s)
	254: 'rpl_luserchannels',	# <integer> :channels formed
	255: 'rpl_luserme',			# :i have <integer> clients and <integer> servers
	256: 'rpl_adminme',			# <server> :administrative info
	257: 'rpl_adminloc1',		# :<admin info>
	258: 'rpl_adminloc2',		# :<admin info>
	259: 'rpl_adminemail',		# :<admin info>
}


class BotBot(object):
	"""
	:author: Anton Zering <synth@lostprofile.de>
	:author: Jules Held <nemesis@creative-heads.org>
	:copyright: 2012, Anton Zering
	:license: Apache License, Version 2.0
	"""

	def __init__(self, host, nick_name, real_name=None):
		""" 
		Constructor for the bot

		:param host: The server address as tuple of (HOST, PORT)
		:param nick_name: Nickname for the bot.
		:param real_name: Real name of the bot. It not provided, the nick is taken as real name.
		"""

		self.d = Debug()
		
		self.host = host
		self.nick_name = nick_name
		
		if real_name:
			self.real_name = real_name
		else:
			self.real_name = nick_name

		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

		self.parser = IRCParser()

	def connect(self, host=None):
		"""
		Connects to the server

		:param host: The server address as tuple of (HOST, PORT).
		"""

		if not host:
			host = self.host

		self.d.info("Connecting to " + str(host))

		# connect to server socket
		self.sock.connect(self.host)

	def disconnect(self):
		"""Disconnects from the server if already connected."""

		if not self.sock:
			return

		self.d.info("Disconnecting from " + str(self.host))
		self.sock.close()

	def send(self, msg):
		"""
		Sends raw messages to the server.

		:param msg: Message to be sent.

		:return: success of the send operation
		"""

		self.d.notice("<< " + msg)
		return self.sock.sendall(msg + "\r\n")

	def quit(self, quit_msg=""):
		"""
		Sends a QUIT command to the server. Then disconnects.

		:param quit_msg: Quit message.
		"""

		self.send('QUIT %s' % quit_msg)
		self.disconnect()

	def join(self, channels):
		"""
		Sends a JOIN message to the server to joins one or multiple channels

		:param channels: One or more channels separated by whitespaces.
		"""

		return self.send('JOIN %s' % channels)

	def part(self, channels, part_msg=None):
		"""
		Sends the PART message to the searver to leave one or multiple channels

		:param channels: One or more channels separated by whitespaces.
		:param part_msg: Part message to appear in the channel
		"""

		return self.send('PART %s :%s' % (channels, part_msg))

	def nick(self, new_nick):
		"""
		Sends the NICK message to the server to try a nickname change of the bot

		:param new_nick: The new nick
		"""

		return self.send("NICK %s" % new_nick)

	def notice(self, target, msg):
		"""
		Sends a NOTICE message to a reciever

		:param target: Reciever of the message
		:param msg: Message to be sent
		"""

		return self.send("NOTICE %s :%s" % (target, msg))

	def msg(self, target, msg):
		"""
		Sends a PRIVMSG message to a channel or another client

		:param target: Reciever of the message. Channel or a nick name.
		:param msg: Message to be sent
		"""
		return self.send("PRIVMSG %s :%s" % (target, msg))

	def on_ping(self, params):
		"""
		Handles PING messages from the server

		"""

		self.send("PONG :%s" % params['text'])

	def exit(self, exit_code=0):
		sys.exit(exit_code)

	def start(self):
		# connect to server
		self.connect()

		# set default nick name
		self.nick(self.nick_name)

		# set default user and real name
		self.send("USER %s 0 0 :%s" % (self.nick_name, self.real_name))
		
		# TODO: move to plugin!
		# Authenticate at Nickserv:
		# self.auth(self.config['password'])

		while True:
			try:
				recv = self.sock.recv(128)
				# print recv
			except:
				self.exit(0)

			for line in recv.split("\n"):
				line = line.rstrip()

				# ignore empty lines
				if not line: continue

				# handle irc commands
				msg = self.parser.parse(line)

				if msg:		
					self.handle_irc(msg)

	def handle_irc(self, msg):
		method = lookup_hook(self, msg.get('cmd'), codes)

		if method:
			return method(msg)