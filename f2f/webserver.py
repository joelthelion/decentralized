#! /usr/bin/env python

from wsgiref.simple_server import make_server

def not_found(environ, start_response):

   response_body="Error 404: Not found"
   status = '404 Not Found'
   start_response(status, [])
   return [response_body]

import re
import submit
import show_links

urls = [
(re.compile(r'^submit$'),submit.submit),
(re.compile(r'^post_link$'),submit.post_link),
(re.compile(r'^show_links$'),show_links.show_links),
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
    port     = 8085
    srv = make_server(hostname, port, dispatcher)
    print 'server started on http://%s:%d/' % (hostname,port)
    srv.serve_forever()

if __name__ == '__main__':
    start_server()
