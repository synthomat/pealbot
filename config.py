# coding: utf-8

"""
:var PATHS: Various paths. I.g. plugins
:var IDENTITY: Identity of the bot as a IRC client
:var HOST: IRC server host as tuple (SERVER, PORT)
:var AUTOJOIN: Channels to autojoin
:var PLUGINS: Autoload these plugins
"""
PATHS = {
	"plugins": "plugins",
}

IDENTITY = {
	'nick': 'pealBot',
	'username': "pbot",
	'realname': 'Awesome Bot',
	#'password': 'XXX',
}

HOST = ('irc.freenode.org', 6667)
AUTOJOIN = ("#randomchan",)


PLUGINS = (
	'basic.Basic',
	#'admin.Admin',
	'aspell.Aspell',
	'reminder.Reminder',
	#'quotes.Quotes',
)