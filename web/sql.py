#!/usr/bin/env python

import MySQLdb

def connect_db():
	return MySQLdb.connect('localhost','test3','abc','prout')

def login_list(db):
	cursor=db.cursor()
	cursor.execute('select * from users')
	return [user[0] for user in cursor.fetchall()]

if __name__=='__main__':
	db=connect_db()
	print login_list(db)
