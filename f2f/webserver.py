#! /usr/bin/env python

from wsgiref.simple_server import make_server
from cgi import parse_qs, escape

html = """
<html>
<body>
   <form method="post" action="parsing_get.wsgi">
      <p>
         Age: <input type="text" name="age">
         </p>
      <p>
         Hobbies:
         <input name="hobbies" type="checkbox" value="software"> Software
         <input name="hobbies" type="checkbox" value="tunning"> Auto Tunning
         </p>
      <p>
         <input type="submit" value="Submit">
         </p>
      </form>
   <p>
      Age: %s<br>
      Hobbies: %s
      </p>
   </body>
</html>"""

def not_found(environ, start_response):

   response_body="Error 404: Not found"
   status = '404 Not Found'
   start_response(status, [])
   return [response_body]

def test_post_page(environ, start_response):

   # the environment variable CONTENT_LENGTH may be empty or missing
   try:
      request_body_size = int(environ.get('CONTENT_LENGTH', 0))
   except (ValueError):
      request_body_size = 0

   # When the method is POST the query string will be sent
   # in the HTTP request body which is passed by the WSGI server
   # in the file like wsgi.input environment variable.
   request_body = environ['wsgi.input'].read(request_body_size)

   response_body=""
   # Sorting and stringifying the environment key, value pairs
   #response_body = ['%s: %s' % (key, value)
   #                 for key, value in sorted(environ.items())]
   #response_body = '<br>'.join(response_body) + '<br>'

   d = parse_qs(request_body)
   age = d.get('age', [''])[0] # Returns the first age value.
   hobbies = d.get('hobbies', []) # Returns a list of hobbies.

   # Always escape user input to avoid script injection
   age = escape(age)
   hobbies = [escape(hobby) for hobby in hobbies]

   response_body = response_body + html % (age or 'Empty',
               ', '.join(hobbies or ['No Hobbies']))

   status = '200 OK'

   response_headers = [('Content-Type', 'text/html'),
                  ('Content-Length', str(len(response_body)))]
   start_response(status, response_headers)

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

   response_headers = [('Content-Type', 'text/html'),
                  ('Content-Length', str(len(response_body)))]
   start_response(status, response_headers)

   return [response_body]

import re

urls = [
(re.compile(r'^$'),test_post_page),
(re.compile(r'^submit$'),submit),
#(re.compile(r'^disliked/$'),disliked),
#(re.compile(r'^hidden/$'),hidden),
#(re.compile(r'^img/(\w+\.png)$'),serve_image),
#(re.compile(r'^css/(\w+\.css)$'),serve_css)
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
