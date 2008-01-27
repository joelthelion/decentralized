#!/usr/bin/env python

import MySQLdb

db=MySQLdb.connect('localhost','test3','abc','prout')
cursor=db.cursor()

cursor.execute('select * from users')
for k,row in enumerate(cursor.fetchall()):
	print k,row

