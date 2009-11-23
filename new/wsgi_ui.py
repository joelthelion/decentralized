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

source_formats = [
(re.compile(r'''^http://www.reddit.com/r/(\w+)/'''),lambda x: x.groups()[0] + "@reddit.com"), #reddit links display subreddit
(re.compile(r'''^http://(\w+\.|)(\w+\.\w+)/'''),lambda x: x.groups()[1])] #rss links with server name display server name
def format_source(source):
    for source_re,source_format in source_formats:
        match = source_re.search(source.source)
        if match is not None:
            return source_format(match)
    return source.source

def format_sources(sources):
    return "<em>" + ", ".join(escape(format_source(source)) for source in sources) + "</em>"

def format_date(delta):
    if delta.days > 0:
        return "%d days ago" % delta.days
    elif delta.seconds > 3600:
        return "%d hours ago" % (delta.seconds/3600)
    elif delta.seconds > 60:
        return "%d minutes ago" % (delta.seconds/60)
    else:
        return "%d seconds ago" % (delta.seconds)

def format_link(k,link):
    now = datetime.now()
    return '''<div class='%(eval)s %(evenodd)s'>
    <div class='buttons'>
        <a href='?action=good&key=%(url)s'><div class='goodbut'></div></a>
        <a href='?action=bad&key=%(url)s'><div class='badbut'></div></a>
        <a href='?action=%(hideact)s&key=%(url)s'><div class='%(hideact)sbut'></div></a></div>
    <div class='contents'>
        <h1><a class='extlink' target='_blank' href=%(urlext)s>%(title)s</a></h1>
        <p>from %(sources)s %(datefromnow)s</p></div>
    <div class='clear'></div>
        </div>''' % {'urlext':quoteattr(link.url),'url':quote_plus(link.url),'title':escape(link.title),'eval':{True:'good',False:'bad',None:'uneval'}[link.evaluation],'hideact':{True:'unhide',False:'hide',None:'hide'}[link.hidden],'evenodd':['even','odd'][k%2],'sources':format_sources(link.sources),'datefromnow':format_date(now-link.date)}

def format_links(links):
    return '''<div class='links'>''' + ''.join(format_link(k,link) for k,link in enumerate(links)) + '''</div>'''

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
    resp = '''<html><head><title>title</title>%(csslink)s</head><body>%(menu)s%(links)s</body></html>''' % {'menu':get_menu(environ),'links':format_links(links),'csslink':get_csslink(environ)}
    start_response('200 OK', [('Content-Type', 'text/html;charset=UTF-8')])
    resp = resp.encode('utf8')
    return [resp]

def index(environ,start_response):
    handle_rating(environ)
    links = cursor.query(Link).filter(db.and_(Link.combined_prediction == True,db.or_(Link.hidden == None,Link.hidden == False))).order_by(Link.evaluation_date.desc()).limit(5).from_self().order_by(Link.evaluation_date.asc()).all() \
          + cursor.query(Link).filter(db.and_(Link.evaluation_date == None,Link.combined_prediction == True,db.or_(Link.hidden == None,Link.hidden == False))).order_by(Link.date.desc()).limit(45).all()
    return display_links(environ,start_response,links)

def liked(environ,start_response):
    handle_rating(environ)
    links = cursor.query(Link).filter(db.and_(Link.evaluation == True,db.or_(Link.hidden == None,Link.hidden == False))).order_by(Link.date.asc()).limit(50).all()
    return display_links(environ,start_response,links)

def disliked(environ,start_response):
    handle_rating(environ)
    links = cursor.query(Link).filter(db.and_(Link.evaluation == False,db.or_(Link.hidden == None,Link.hidden == False))).order_by(Link.date.asc()).limit(50).all()
    return display_links(environ,start_response,links)

def hidden(environ,start_response):
    handle_rating(environ)
    links = cursor.query(Link).filter(Link.hidden == True).order_by(Link.date.desc()).limit(50).all()
    return display_links(environ,start_response,links)

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

def dispatcher(environ,start_response):
    urls = [ (re.compile(r'^$'),index), (re.compile(r'^liked/$'),liked), (re.compile(r'^disliked/$'),disliked), (re.compile(r'^hidden/$'),hidden), (re.compile(r'^img/(\w+\.png)$'),serve_image), (re.compile(r'^css/(\w+\.css)$'),serve_css) ]
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

