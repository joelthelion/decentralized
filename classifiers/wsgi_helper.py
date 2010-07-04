'''this module contains functions helper for the wsgi gui'''

import re
from datamodel import Link
from cgi import parse_qs
from datetime import datetime
from xml.sax.saxutils import escape,quoteattr
from urllib import quote_plus
from database import Session
from wsgi_prefs import prefs
cursor = Session()

def parse_rating(environ,indent="++ "):
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

def handle_rating(function):
    '''decorator for handler that parse url for rating'''
    def wrapper(environ,start_response):
        parse_rating(environ)
        return function(environ,start_response)
    return wrapper
    

source_formats = [
(re.compile(r'''^http://www.reddit.com/r/(\w+)/'''),lambda x: x.groups()[0] + "@reddit.com"), #reddit links display subreddit
(re.compile(r'''^http://(\w+\.|)(\w+\.\w+)/'''),lambda x: x.groups()[1]) #rss links with server name display server name
]
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
        <a href='?action=good&key=%(url)s'><div class='goodbut'>G</div></a>
        <a href='?action=bad&key=%(url)s'><div class='badbut'>B</div></a>
        <a href='?action=%(hideact)s&key=%(url)s'><div class='%(hideact)sbut'>H</div></a></div>
    <div class='contents'>
        <h1><a class='extlink' target='_blank' href=%(urlext)s>%(title)s</a></h1>
        <p>from %(sources)s %(datefromnow)s</p></div>
    <div class='clear'></div>
        </div>''' % {'urlext':quoteattr(link.url),'url':quote_plus(link.url),'title':escape(link.title),'eval':{True:'good',False:'bad',None:'uneval'}[link.evaluation],'hideact':{True:'unhide',False:'hide',None:'hide'}[link.hidden],'evenodd':['even','odd'][k%2],'sources':format_sources(link.sources),'datefromnow':format_date(now-link.date)}

def format_links(links):
    return '''<div class='links'>''' + ''.join(format_link(k,link) for k,link in enumerate(links)) + '''</div>'''

def get_csslink(environ):
    parameters = parse_qs(environ.get('QUERY_STRING', ''))
    if 'css' in parameters: prefs.set("cssfilename",parameters['css'][0])
    return '''<link rel='stylesheet' type='text/css' href='/css/%s' />''' % escape(prefs.get("cssfilename"))

def get_menu(environ):
    return '''<p class='menuright'><a href='?css=pierre.css'>pierre.css</a> <a href='?css=joel.css'>joel.css</a></p><p class='menu'><a href='/'>home</a> <a href='/liked/'>liked</a> <a href='/disliked/'>disliked</a> <a href='/hidden/'>hidden</a></p>'''

def display_links(environ, start_response,links):
    '''display link helper'''
    resp = '''<html><head><title>Hermie the brave news helper</title>%(csslink)s</head><body>%(menu)s%(links)s</body></html>''' % {'menu':get_menu(environ),'links':format_links(links),'csslink':get_csslink(environ)}
    start_response('200 OK', [('Content-Type', 'text/html;charset=UTF-8')])
    resp = resp.encode('utf8')
    return [resp]

def return_links(function):
    '''decorator function that lift link list to html page'''
    def wrapper(environ,start_response):
        links = function()
        return display_links(environ,start_response,links)
    return wrapper

