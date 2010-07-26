from cgi import parse_qs, escape

#TODO: replace stuff to make a configuration page

submit_html= """
<html>
<title>Submit a link</title>
<body>
    <h3>Submit a link</h3>
   <form method="post" action="post_link">
      <p>
         Jabber id: <input type="text" name="jid" value="%s">
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
   url = escape(d.get('url', ['http://www.google.com'])[0])
   title = escape(d.get('title', ['No title.'])[0])

   from daemon import post_queue
   from post import Post
   mypost=Post()
   mypost.url=url
   mypost.title=title
   post_queue.put(mypost)

   response_body=post_link_html % url
   response_headers = [('Content-Type', 'text/html;charset=utf-8'),
                  ('Content-Length', str(len(response_body)))]
   start_response('200 OK', response_headers)
   return [response_body]
