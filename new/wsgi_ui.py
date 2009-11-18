#!/usr/bin/env python

from datamodel import *
from cgi import parse_qs
from urllib import quote_plus
from xml.sax.saxutils import escape,quoteattr
from datetime import datetime
import time
import re
import database as db
cursor = db.Session()


def format_link(link):
    return '''<li class='%(eval)s'><a href='?action=good&key=%(url)s'>good</a> <a href='?action=bad&key=%(url)s'>bad</a> <a href=%(urlext)s>%(title)s</a> <a href='?action=%(hideact)s&key=%(url)s'>%(hideact)s</a> </li>''' % {'urlext':quoteattr(link.url),'url':quote_plus(link.url.encode('utf-8')),'title':escape(link.title),'eval':{True:'good',False:'bad',None:'uneval'}[link.evaluation],'hideact':{True:'unhide',False:'hide',None:'hide'}[link.hidden]}

def map_links_to_lu(links):
    return '''<lu class='links'>''' + ''.join(format_link(link) for link in links) + '''</lu>'''

def get_csslink(environ):
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    cssfilename = 'default.css'
    if 'css' in parameters: cssfilename = escape(parameters['css'][0])
    return '''<link rel='stylesheet' type='text/css' href='/css/%s' />''' % cssfilename

def get_menu(environ):
    return '''<p class='menu'><a href='/'>home</a> <a href='/liked/'>liked</a> <a href='/disliked/'>disliked</a> <a href='/hidden/'>hidden</a></p>'''

def handle_rating(environ):
    '''parse query string and update vote and hidden state'''
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    if 'action' not in parameters or 'key' not in parameters: return

    link = cursor.query(Link).get(parameters['key'][0].decode('utf8'))
    if link is None: 
        print "unknown link %s" % parameters['key'][0].decode('utf8')
        return

    action = parameters['action'][0]
    if   action == 'hide':   print 'hidding %s'   % link.url; link.hidden = True
    elif action == 'unhide': print 'showing %s'   % link.url; link.hidden = False
    elif action == 'good':   print 'good link %s' % link.url; link.evaluation = True;  link.evaluation_date=datetime.now();
    elif action == 'bad':    print 'bad link %s'  % link.url; link.evaluation = False; link.evaluation_date=datetime.now();
    else: print "unknow action %s" % action
    cursor.commit()
    
def display_links(environ, start_response,links):
    '''display link helper'''
    resp = '''<html><head><title>Hermie the brave news helper</title>%(csslink)s</head><body>%(menu)s%(links)s</body></html>''' % {'menu':get_menu(environ),'links':map_links_to_lu(links),'csslink':get_csslink(environ)}
    start_response('200 OK', [('Content-Type', 'text/html;charset=UTF-8')])
    resp = resp.encode('utf8')
    return [resp]

def index(environ,start_response):
    handle_rating(environ)
    links = cursor.query(Link).filter(db.and_(Link.evaluation_date == None,Link.combined_prediction == True,db.or_(Link.hidden == None,Link.hidden == False))).order_by(Link.date.desc()).limit(50).all()
    return display_links(environ,start_response,links)

def liked(environ,start_response):
    handle_rating(environ)
    links = cursor.query(Link).filter(db.and_(Link.evaluation == True,db.or_(Link.hidden == None,Link.hidden == False))).order_by(Link.evaluation_date.desc()).limit(50).all()
    return display_links(environ,start_response,links)

def disliked(environ,start_response):
    handle_rating(environ)
    links = cursor.query(Link).filter(db.and_(Link.evaluation == False,db.or_(Link.hidden == None,Link.hidden == False))).order_by(Link.evaluation_date.desc()).limit(50).all()
    return display_links(environ,start_response,links)

def hidden(environ,start_response):
    handle_rating(environ)
    links = cursor.query(Link).filter(Link.hidden == True).order_by(Link.date.desc()).limit(50).all()
    return display_links(environ,start_response,links)

def css(environ, start_response):
    '''serve css files'''
    try:
        cssfile = open(environ.get('URL_ARGS','')[0],'r')
        resp = cssfile.read()
        start_response('200 OK', [('Content-Type', 'text/css;charset=UTF-8')])
        resp = resp.encode('utf8')
        return [resp]
    except IOError:
        return not_found(environ,start_response)

def not_found(environ, start_response):
    '''404 error handler'''
    start_response('404 NOT FOUND', [('Content-Type', 'text/plain;charset=UTF-8')])
    return ['Not Found']

def dispatcher(environ,start_response):
    urls = [ (re.compile(r'^$'),index), (re.compile(r'^liked/$'),liked), (re.compile(r'^disliked/$'),disliked), (re.compile(r'^hidden/$'),hidden), (re.compile(r'^css/(\w+\.css)$'),css) ]
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

