#!/usr/bin/env python

import re
from database import and_,or_
from datamodel import Link
from wsgi_helper import handle_rating,return_links,cursor

@handle_rating
@return_links
def index():
    return cursor.query(Link).filter(and_(Link.combined_prediction == True,or_(Link.hidden == None,Link.hidden == False))).order_by(Link.evaluation_date.desc()).limit(5).from_self().order_by(Link.evaluation_date.asc()).all() \
         + cursor.query(Link).filter(and_(Link.evaluation_date == None,Link.combined_prediction == True,or_(Link.hidden == None,Link.hidden == False))).order_by(Link.date.desc()).limit(45).all()

@handle_rating
@return_links
def liked():
    return cursor.query(Link).filter(and_(Link.evaluation == True,or_(Link.hidden == None,Link.hidden == False))).order_by(Link.date.asc()).limit(50).all()

@handle_rating
@return_links
def disliked():
    return cursor.query(Link).filter(and_(Link.evaluation == False,or_(Link.hidden == None,Link.hidden == False))).order_by(Link.date.asc()).limit(50).all()

@handle_rating
@return_links
def hidden():
    return cursor.query(Link).filter(Link.hidden == True).order_by(Link.date.desc()).limit(50).all()

def serve_css(environ, start_response):
    '''serve css files'''
    try:
        cssfile = open(environ.get('URL_ARGS','')[0],'r')
        resp = cssfile.read()
        cssfile.close()
        start_response('200 OK', [('Content-Type', 'text/css;charset=UTF-8')])
        resp = resp.encode('utf8')
        return [resp]
    except IOError:
        return not_found(environ,start_response)

def serve_image(environ, start_response):
    '''serve images files'''
    try:
        imgfile = open(environ.get('URL_ARGS','')[0],'rb')
        resp = imgfile.read()
        imgfile.close()
        start_response('200 OK', [('Content-Type', 'image/png')])
        return [resp]
    except IOError:
        return not_found(environ,start_response)

def not_found(environ, start_response):
    '''404 error handler'''
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain;charset=UTF-8')])
    return ['Not Found']

urls = [
(re.compile(r'^$'),index),
(re.compile(r'^liked/$'),liked),
(re.compile(r'^disliked/$'),disliked),
(re.compile(r'^hidden/$'),hidden),
(re.compile(r'^img/(\w+\.png)$'),serve_image),
(re.compile(r'^css/(\w+\.css)$'),serve_css)
]
def dispatcher(environ,start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex,callback in urls:
        match = regex.search(path)
        if match is not None:
            environ['URL_ARGS'] = match.groups()
            return callback(environ, start_response)
    return not_found(environ, start_response)

if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    hostname = 'localhost'
    port     = 8080
    srv = make_server(hostname, port, dispatcher)
    print 'server started on http://%s:%d/' % (hostname,port)
    srv.serve_forever()

