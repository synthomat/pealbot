#!/usr/bin/env python
# coding: utf-8

import unittest

from pealbot import IRCMessage

class IRCParserTest(unittest.TestCase):
	"""
	def setUp(self):
		self.p = IRCParser()
	"""

	def test_parse_error(self):
		msg = IRCMessage.parse("asdf")
		self.assertIsNone(msg)

	def test_parse_successfull(self):
		msg = IRCMessage.parse("PING :kornbluth.freenode.net")
		self.assertIsNotNone(msg)
		self.assertEquals(msg.cmd, 'ping')
		self.assertIsNotNone(msg.trail)
		self.assertEquals(msg.trail, 'kornbluth.freenode.net')

	def test_privmsg(self):
		msg = IRCMessage.parse(":synthom!~synth@kornbluth.freenode.net PRIVMSG botbot :Test String")

		self.assertEquals(msg.nick, 'synthom')
		self.assertEquals(msg.user, 'synth')
		self.assertEquals(msg.host, 'kornbluth.freenode.net')
		self.assertEquals(msg.cmd, 'privmsg')
		self.assertEquals(msg.targets, ['botbot'])
		self.assertEquals(msg.trail, 'Test String')


from lib.tools import lookup_hook

class LookupHookTest(unittest.TestCase):
	class TestClass(object):
		"""Test class with no funktion. Just for method look ups ;-)"""

		def on_361(self):
			pass

		def on_named(self):
			pass

		def on_looked_up(self):
			pass

	def setUp(self):
		self.tc = self.TestClass()

	def test_method_not_found(self):
		self.assertIsNone(lookup_hook(self.tc, "DOES_NOT_EXISTS"))

	def test_method_number(self):
		m = lookup_hook(self.tc, "361")

		self.assertIsNotNone(m)
		self.assertEquals(m, self.tc.on_361)

	def test_method_named(self):
		m = lookup_hook(self.tc, "named")

		self.assertIsNotNone(m)
		self.assertEquals(m, self.tc.on_named)


if __name__ == '__main__':
    unittest.main()