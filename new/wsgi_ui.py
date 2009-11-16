#!/usr/bin/env python

from datamodel import *
from cgi import parse_qs, escape
from datetime import datetime
import time

def format_link(link):
    return '''<li><a href='?rating=good&key=%s'>good</a> <a href='?rating=bad&key=%s'>bad</a> <a href='%s'>%s</a></li>''' % tuple(map(escape,(link.url,link.url,link.url,link.title)))

def map_links_to_lu(links):
    return '<lu>' + ''.join(format_link(link) for link in links) + '</lu>'

cursor = None
def hello_world(environ, start_response):
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    if 'subject' in parameters:
        subject = escape(parameters['subject'][0])
    else:
        subject = u'World'
    start_response('200 OK', [('Content-Type', 'text/html;charset=UTF-8')])

    fresh = cursor.query(Link).filter(Link.evaluation_date == None).\
        filter_by(combined_prediction=True).\
        order_by(Link.date.desc()).limit(10).all()
    resp = '''<html><head><title>title</title></head><body><p>Hello %(subject)s!</p> %(fresh)s </body></html>''' % {'subject': subject, 'fresh': map_links_to_lu(fresh)}
    resp = resp.encode('utf8')
    return [resp]

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    import database as db

    cursor = db.Session()

    hostname = 'localhost'
    port     = 8080
    srv = make_server(hostname, port, hello_world)
    print "server started on http://%s:%d/" % (hostname,port)
    srv.serve_forever()

