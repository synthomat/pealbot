#!/usr/bin/env python
# coding: utf-8

import unittest

from lib.parser import IRCParser

class IRCParserTest(unittest.TestCase):

	def setUp(self):
		self.p = IRCParser()

	def test_parse_error(self):
		msg = self.p.parse("asdf")
		self.assertIsNone(msg)

	def test_parse_successfull(self):
		msg = self.p.parse("PING :kornbluth.freenode.net")
		self.assertIsNotNone(msg)
		self.assertEquals(msg.get('cmd'), 'ping')
		self.assertIsNotNone(msg.get('text'))
		self.assertEquals(msg.get('text'), 'kornbluth.freenode.net')

	def test_privmsg(self):
		msg = self.p.parse(":synthom!~synth@kornbluth.freenode.net PRIVMSG botbot :Test String")

		self.assertEquals(msg.get('nick'), 'synthom')
		self.assertEquals(msg.get('user'), 'synth')
		self.assertEquals(msg.get('host'), 'kornbluth.freenode.net')
		self.assertEquals(msg.get('cmd'), 'privmsg')
		self.assertEquals(msg.get('dest'), ['botbot'])
		self.assertEquals(msg.get('text'), 'Test String')

	def test_parse_get_default(self):
		# test none as default parameter if key was not found
		self.assertIsNone(self.p.get('does_not_exists'))

		# test default parameter if key was not found
		self.assertEqual(self.p.get('does_not_exists', '#channel'), '#channel')

if __name__ == '__main__':
    unittest.main()