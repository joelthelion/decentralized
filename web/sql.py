#!/usr/bin/env python

import MySQLdb

def connect_db():
	return MySQLdb.connect('localhost','test3','abc','prout')

def query(query,db):
	try:
		db.query(query)
		return True
	except:
		print "query error: %s..." % db.error()
		return False
	
#user oriented
def login_list(db):
		cursor=db.cursor()
		cursor.execute('select login from kolmognus_user')
		return [user[0] for user in cursor.fetchall()]

def login_test(login,password,db):
	try:
		cursor=db.cursor()
		cursor.execute("select login from kolmognus_user where login='%s' and pass=PASSWORD('%s')" % (login,password))
		return cursor.rowcount==1
	except:
		print "query error: %s..." % db.error()
		return False

if __name__=='__main__':
	db=connect_db()
	print login_list(db)
