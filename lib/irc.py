import re

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