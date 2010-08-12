#! /usr/bin/env python

from wsgiref.simple_server import make_server
from persistence import PersistentObject,basedir

class FriendStorageObject(PersistentObject):
     storage_file=basedir+"friendserver.pck"
     def __init__(self):
        PersistentObject.__init__(self)
        if not self.__dict__.has_key("friends"):
            self.friends=[]

storage=FriendStorageObject()

def not_found(environ, start_response):
   response_body="Error 404: Not found"
   status = '404 Not Found'
   print environ
   start_response(status, [])
   return [response_body]

get_friends_html= """
<html>
<title>Here are some friends!</title>
<body>
%s
</body>
</html>"""

def get_friends(environ,start_response):
    pass

def post(environ,start_response):
    d = parse_qs(environ['QUERY_STRING'])
    jid = escape(d.get('jid', [''])[0])
    ip = environ['REMOTE_ADDR']
    storage.friends.append((jid,ip))

import re

urls = [
(re.compile(r'^get_friends$'),get_friends),
(re.compile(r'^post$'),post),
]

def dispatcher(environ,start_response):
    path = environ.get('PATH_INFO', '').lstrip('/')
    for regex,callback in urls:
        match = regex.search(path)
        if match is not None:
            environ['URL_ARGS'] = match.groups()
            return callback(environ, start_response)
    return not_found(environ, start_response)

def start_server():
    from wsgiref.simple_server import make_server
    hostname = 'localhost'
    port     = 8084
    srv = make_server(hostname, port, dispatcher)
    print 'server started on http://%s:%d/' % (hostname,port)
    srv.serve_forever()

if __name__ == '__main__':
    start_server()
