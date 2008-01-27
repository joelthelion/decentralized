#!/usr/bin/env python

import MySQLdb

def connect_db():
	return MySQLdb.connect('localhost','test3','abc','prout')

def login_exists(login,db):
	cursor=db.cursor()
	return cursor.execute("select * from users where login='%s'" % login)==1

def login_list(db):
	cursor=db.cursor()
	cursor.execute('select * from users')
	return [user[0] for user in cursor.fetchall()]

def login_paswd_test(login,password,db):
	cursor=db.cursor()
	return cursor.execute("select * from users where login='%s' and pass=PASSWORD('%s')" % (login,password))

if __name__=='__main__':
	db=connect_db()
	print login_list(db)
