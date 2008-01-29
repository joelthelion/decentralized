#!/usr/bin/env python

import sql

#param number decorator
def as_param_number(n_params):
	def test_param(func):
		def new_func(params,db):
			if len(params)>=n_params or n_params<0:
				return func(params,db)
			else:
				return func.__name__+func.__doc__
		new_func.__name__=func.__name__
		new_func.__doc__=func.__doc__
		return new_func
	return test_param

#commands implementation
#help
@as_param_number(0)
def usage(params,db):
	""": display commands help"""
	functions={}
	for command,function in commands.items():
		if function in functions:
			functions[function].append(command)
		else:
			functions[function]=[command]
	return '\n'.join([','.join(cmds)+function.__doc__ for function,cmds in functions.items()])

#fetcher oriented command
@as_param_number(1)
def addtag(params,db):
	""" tag: add tag to fetcher"""
	pass

#user oriented command
@as_param_number(2)
def adduser(params,db):
	""" login password: add user to database"""
	login=params[0]
	passwd=params[1]

	#add user
	if sql.query("insert into kolmognus_user (login,pass) values ('%s',PASSWORD('%s'))" % (login,passwd),db):
		return  "user %s added to database" % login  
	else:
		return "can't add user %s..." % login

@as_param_number(1)
def remuser(params,db):
	""" login: remove user from database"""
	login=params[0]

	#remove user
	if sql.query("delete from kolmognus_user where login='%s'" % login,db):
		return "user %s removed from database" % login
	else:
		return "can't remove user %s: not in database..." % login
		
@as_param_number(2)
def testlogin(params,db):
	""" login password: test password for user"""
	login=params[0]
	password=params[1]

	if sql.login_test(login,password,db):
		return "password ok"
	else:
		return "password err"

@as_param_number(0)
def listuser(params,db):
	""": list users in database"""
	return "users: "+" ".join(sql.login_list(db))

@as_param_number(0)
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
