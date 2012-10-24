import re
import socket
import sys

codes = {
	376: "end_of_motd"
}

class BotBot(object):
	def __init__(self, config):
		self.config = config
		self.sock = None
		self.re_msg = re.compile(r":(?P<host>.+) (?P<cmd>.+) (?P<dest>.*) :(?P<text>.*)")
		self.re_cmd = re.compile(r"(?P<cmd>.+) :(?P<text>.*)")

		self.buffer = []

	def connect(self, server=None):
		print "- connecting to", server
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.sock.connect(self.config['server'])

	def disconnect(self):
		if self.sock:
			print "- disconnecting from", self.config['server']
			self.sock.close()
			sys.exit(0)

	def on_end_of_motd(self, params):
		self.join(self.config['autojoin'])

	def quit(self, quit_msg=None):
		self.send('QUIT %s' % quit_msg)
		self.disconnect()

	def join(self, channels):
		self.send('JOIN %s' % channels)

	def part(self, channels, quit_msg=None):
		pass

	def nick(self, new_nick):
		self.send("NICK %s" % new_nick)

	def notice(self, dest, msg):
		pass

	def send(self, msg):
		print "<< " + msg
		self.sock.sendall(msg + "\r\n")

	def msg(self, target, text):
		self.send("PRIVMSG %s :%s" % (target, text))

	def on_ping(self, params):
		self.send("PONG :%s" % params['text'])

	def start(self):
		self.connect(self.config['server'])

		# set default nick name
		self.nick(self.config['nick'])

		# set default user and real name
		self.send("USER %s 0 0 :%s" % (self.config['nick'], self.config['realname']))

		while True:
			recv = self.sock.recv(2048)

			self.buffer = recv.split("\n")

			for line in self.buffer:
				line = line.rstrip("\r\n")

				# ignore empty lines
				if not line:
					continue

				# local echo
				# print line

				# handle irc commands
				self.handle_irc(line)

			self.buffer = []

	def handle_irc(self, recv):
		msg_parts = {}

		if recv.startswith(':'):
			msg_match = self.re_msg.match(recv)
		else:
			msg_match = self.re_cmd.match(recv)
		
		if not msg_match:
			return 
		
		msg_parts = msg_match.groupdict()
		cmd = msg_parts['cmd'].lower()

		if cmd.isdigit() and int(cmd) in codes:
			method = "on_" + codes[int(cmd)]
		else:
			method = "on_" + cmd

		if method in dir(self):
			self.invoke_hook(method, msg_parts)

	def invoke_hook(self, method, msg_parts):
		m = getattr(self, method)
		if m:
			print "--- Handling %s" % method
			m(msg_parts)