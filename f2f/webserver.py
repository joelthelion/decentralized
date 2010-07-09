#! /usr/bin/env python

from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

def not_found(environ, start_response):

   response_body="Error 404: Not found"
   status = '404 Not Found'
   start_response(status, [])
   return [response_body]

submit_html= """
<html>
<title>Submit a link</title>
<body>
    <h3>Submit a link</h3>
   <form method="post" action="post_link">
      <p>
         Title: <input type="text" name="title" value="%s">
         </p>
      <p>
         URL:
            <input type="text" name="url" value="%s">
         </p>
      <p>
         <input type="submit" value="Submit">
         </p>
      </form>
   </body>
</html>"""

def submit(environ,start_response):
   # Get method: Returns a dictionary containing lists as values.
   d = parse_qs(environ['QUERY_STRING'])
   url = escape(d.get('url', [''])[0])
   title = escape(d.get('title', [''])[0])

   response_body = submit_html % (title,url or 'http://')
   status = '200 OK'

   response_headers = [('Content-Type', 'text/html;charset=utf-8'),
                  ('Content-Length', str(len(response_body)))]
   start_response(status, response_headers)

   return [response_body]

post_link_html= """
<html>
<meta HTTP-EQUIV="Refresh" content="1;URL=%s"> 
<title>Submission posted!</title>
<body>
Your submission has been succesfully posted!
</body>
</html>"""

def post_link(environ,start_response):
   try:
      request_body_size = int(environ.get('CONTENT_LENGTH', 0))
   except (ValueError):
      request_body_size = 0
   request_body = environ['wsgi.input'].read(request_body_size)
   d = parse_qs(request_body)
   url = escape(d.get('url', ['http://www.google.com'])[0]) # Returns the first age value.
   response_body=post_link_html % url
   response_headers = [('Content-Type', 'text/html;charset=utf-8'),
                  ('Content-Length', str(len(response_body)))]
   start_response('200 OK', response_headers)
   return [response_body]

import re

urls = [
(re.compile(r'^submit$'),submit),
(re.compile(r'^post_link$'),post_link)
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
