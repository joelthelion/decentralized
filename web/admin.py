#!/usr/bin/env python

import sql

#commands implementation
def usage(params,db):
	""": display commands help"""
	functions={}
	for command,function in commands.items():
		if function in functions:
			functions[function].append(command)
		else:
			functions[function]=[command]
	return '\n'.join([','.join(cmds)+function.__doc__ for function,cmds in functions.items()])

def adduser(params,db):
	""" login password: add user to database"""
	#parse parameters
	if len(params)!=2:
		return "adduser"+adduser.__doc__
	else:
		login=params[0]
		passwd=params[1]

	#add user
	if sql.login_exists(login,db):
		return "can't add user %s: already in database..." % login
	else:
		db.query("insert into users (login,pass) values ('%s',PASSWORD('%s'))" % (login,passwd))
		return  "user %s added to database" % login  

def remuser(params,db):
	""" login: remove user from database"""
	#parse parameters
	if len(params)!=1:
		return "remuser"+remuser.__doc__
	else:
		login=params[0]

	#remove user
	if not sql.login_exists(login,db):
		return "can't remove user %s: not in database..." % login
	else:
		db.query("delete from users where login='%s'" % login)
		return "user %s removed from database" % login

def testlogin(params,db):
	""" login password: test password for user"""
	#parse parameters
	if len(params)!=2:
		return "testlogin"+testlogin.__doc__
	else:
		login=params[0]
		passwd=params[1]

	if sql.login_paswd_test(login,passwd,db):
		return "password ok"
	else:
		return "password err"

def listuser(params,db):
	""": list users in database"""
	return " ".join(sql.login_list(db))

def quit(params,db):
	""": quit the command line"""
	import sys
	sys.exit()
	return "quitting..."

#commands binding
commands={
	'quit'		: quit,
	'q'		: quit,
	'listuser'	: listuser,
	'list'  	: listuser,
	'ls'		: listuser,
	'adduser'	: adduser,
	'add'		: adduser,
	'remuser'	: remuser,
	'rm'		: remuser,
	'usage'		: usage,
	'help'		: usage,
	'h'		: usage,
	'testlogin'	: testlogin,
	'test'		: testlogin}

#user interface
def get_command():
	while True:
		words=[word for word in raw_input('kolmognus$').split(' ') if word]
		if len(words)==1:
			return words[0],[]
		elif len(words)>1:
			return words[0],words[1:]

def main():
	#connect to database
	db=sql.connect_db()

	#main loop
	while True:
		try:
			action,params=get_command()
		except EOFError:
			break
		try:
			print commands[action](params,db)
		except KeyError:
			print "unknow command %s..." % action

if __name__=='__main__':
	main()
