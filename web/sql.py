#!/usr/bin/env python

import MySQLdb

db = MySQLdb.connect('localhost','test3','abc','prout')

def query(query):
	try:
		db.query(query)
		return True
	except:
		print "query error: %s..." % db.error()
		return False

def request(request):
    try:
        cursor=db.cursor()
        cursor.execute(request)
        return cursor.fetchall()
    except:
        print "query error: %s..." % db.error()
        return False
        
	
#user oriented
def login_list():
		cursor=db.cursor()
		cursor.execute('select login from kolmognus_user')
		return [user[0] for user in cursor.fetchall()]

def login_test(login,password):
	try:
		cursor=db.cursor()
		cursor.execute("select login from kolmognus_user where login='%s' and pass=PASSWORD('%s')" % (login,password))
		return cursor.rowcount==1
	except:
		print "query error: %s..." % db.error()
		return False

#service oriented
def service_list():
		cursor=db.cursor()
		cursor.execute('select name,status from service')
		return cursor.fetchall()

def service_set_status(service,status):
		return query("update service set status='%s' where name='%s'" % (status,service))

#fetcher oriented
def tag_list():
		cursor=db.cursor()
		cursor.execute('select name from tag')
		return [tag[0] for tag in cursor.fetchall()]

if __name__=='__main__':
	print login_list()
