# coding: utf-8
"""
Copyright (c) 2012
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
__all__ = ['Debug', 'lookup_hook', 'irc_codes']

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

irc_codes = {
	##
	## error codes
	##
	'401': 'err_nosuchnick',
	'402': 'err_nosuchserver',
	'403': 'err_nosuchchannel',
	'404': 'err_cannotsendtochan',
	'405': 'err_toomanychannels',
	'406': 'err_wasnosuchnick',
	'407': 'err_toomanytargets',
	'409': 'err_noorigin',
	'411': 'err_norecipient',
	'412': 'err_notexttosend',
	'413': 'err_notoplevel',
	'414': 'err_wildtoplevel',
	'421': 'err_unknowncommand',
	'422': 'err_nomotd',
	'423': 'err_noadmininfo',
	'424': 'err_fileerror',
	'431': 'err_nonicknamegiven',
	'432': 'err_erroneusnickname',
	'433': 'err_nicknameinuse',
	'436': 'err_nickcollision',
	'441': 'err_usernotinchannel',
	'442': 'err_notonchannel',
	'443': 'err_useronchannel',
	'444': 'err_nologin',
	'445': 'err_summondisabled',
	'446': 'err_usersdisabled',
	'451': 'err_notregistered',
	'461': 'err_needmoreparams',
	'462': 'err_alreadyregistred',
	'463': 'err_nopermforhost',
	'464': 'err_passwdmismatch',
	'465': 'err_yourebannedcreep',
	'467': 'err_keyset',
	'471': 'err_channelisfull',
	'472': 'err_unknownmode',
	'473': 'err_inviteonlychan',
	'474': 'err_bannedfromchan',
	'475': 'err_badchannelkey',
	'481': 'err_noprivileges',
	'482': 'err_chanoprivsneeded',
	'483': 'err_cantkillserver',
	'491': 'err_nooperhost',
	'501': 'err_umodeunknownflag',
	'502': 'err_usersdontmatch',

	##
	## command responses
	##
	'300': 'rpl_none',
	'302': 'rpl_userhost',
	'303': 'rpl_ison',
	'301': 'rpl_away',
	'305': 'rpl_unaway',
	'306': 'rpl_nowaway',
	'311': 'rpl_whoisuser',
	'312': 'rpl_whoisserver',
	'313': 'rpl_whoisoperator',
	'317': 'rpl_whoisidle',
	'318': 'rpl_endofwhois',
	'319': 'rpl_whoischannels',
	'314': 'rpl_whowasuser',
	'369': 'rpl_endofwhowas',
	'321': 'rpl_liststart',
	'322': 'rpl_list',
	'323': 'rpl_listend',
	'324': 'rpl_channelmodeis',
	'331': 'rpl_notopic',
	'332': 'rpl_topic',
	'341': 'rpl_inviting',
	'342': 'rpl_summoning',
	'351': 'rpl_version',
	'352': 'rpl_whoreply',
	'315': 'rpl_endofwho',
	'353': 'rpl_namreply',
	'366': 'rpl_endofnames',
	'364': 'rpl_links',
	'365': 'rpl_endoflinks',
	'367': 'rpl_banlist',
	'368': 'rpl_endofbanlist',
	'371': 'rpl_info',
	'374': 'rpl_endofinfo',
	'375': 'rpl_motdstart',
	'372': 'rpl_motd',
	'376': 'rpl_endofmotd',
	'381': 'rpl_youreoper',
	'382': 'rpl_rehashing',
	'391': 'rpl_time',
	'392': 'rpl_usersstart',
	'393': 'rpl_users',
	'394': 'rpl_endofusers',
	'395': 'rpl_nousers',
	'200': 'rpl_tracelink',
	'201': 'rpl_traceconnecting',
	'202': 'rpl_tracehandshake',
	'203': 'rpl_traceunknown',
	'204': 'rpl_traceoperator',
	'205': 'rpl_traceuser',
	'206': 'rpl_traceserver',
	'208': 'rpl_tracenewtype',
	'261': 'rpl_tracelog',
	'211': 'rpl_statslinkinfo',
	'212': 'rpl_statscommands',
	'213': 'rpl_statscline',
	'214': 'rpl_statsnline',
	'215': 'rpl_statsiline',
	'216': 'rpl_statskline',
	'218': 'rpl_statsyline',
	'219': 'rpl_endofstats',
	'241': 'rpl_statslline',
	'242': 'rpl_statsuptime',
	'243': 'rpl_statsoline',
	'244': 'rpl_statshline',
	'221': 'rpl_umodeis',
	'251': 'rpl_luserclient',
	'252': 'rpl_luserop',
	'253': 'rpl_luserunknown',
	'254': 'rpl_luserchannels',
	'255': 'rpl_luserme',
	'256': 'rpl_adminme',
	'257': 'rpl_adminloc1',
	'258': 'rpl_adminloc2',
	'259': 'rpl_adminemail',
}

def lookup_hook(context, name, prefix="on_"):
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
	elif str(name).isdigit() and int(name) in irc_codes:
		name = int(name)

		# resolve code to hook name
		method_name = prefix + irc_codes[name]

		# hook name exists in context?
		if method_name in dir(context):
			return getattr(context, prefix + lookup_table[name])

	return None