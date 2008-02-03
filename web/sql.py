#!/usr/bin/env python

import MySQLdb

db=MySQLdb.connect(host='localhost',user='test3',passwd='abc',db='prout',use_unicode=True,charset="utf8")
#db = MySQLdb.connect('localhost','test3','abc','prout')

def query(query):
    from _mysql_exceptions import ProgrammingError
    try:
        #print "query",type(query)
        db.query(query.encode('utf-8'))
        #db.query(query)
        return True
    except ProgrammingError:
        print "'%s' query error: %s..." % (query,db.error())
        return False

def request(request):
    from _mysql_exceptions import ProgrammingError
    try:
        #print "request", type(request)
        cursor=db.cursor()
        cursor.execute(request.encode('utf-8'))
        #cursor.execute(request)
        results = cursor.fetchall()
        return results
    except ProgrammingError:
        print "'%s' request error: %s..." % (request,db.error())
        return []
    
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
def feed_list():
        cursor=db.cursor()
        cursor.execute('select url from feed')
        return [url[0] for url in cursor.fetchall()]

if __name__=='__main__':
    print login_list()
