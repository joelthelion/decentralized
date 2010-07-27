from cgi import parse_qs, escape
from daemon import storage

#TODO: replace stuff to make a configuration page

config_html= """
<html>
<title>Configuration</title>
<body>
    <h3>Configuration</h3>
   <form method="post" action="post_config">
      <p>
         Jabber id: <input type="text" id="jabber_id" value="%s">
         </p>
      <p>
         Password:
            <input type="password" id="jabber_password" value="%s">
         </p>
         <input type="hidden" id="old_url" value="%s">
      <p>
         <input type="submit" value="Save configuration">
         </p>
      </form>
   </body>
</html>"""

def config_page(environ,start_response):
   previous_url = environ.get('HTTP_REFERER','http://www.google.com')
   response_body = config_html % (storage.config.get("jabber_id","example@example.com"),\
                                  storage.config.get("jabber_password","xxx"),\
                                  previous_url)
   status = '200 OK'
   response_headers = [('Content-Type', 'text/html;charset=utf-8'),
                  ('Content-Length', str(len(response_body)))]
   start_response(status, response_headers)
   return [response_body]

post_config_html= """
<html>
<!-- <meta HTTP-EQUIV="Refresh" content="1;URL=%s">  -->
<title>Configuration updated!</title>
<body>
Your configuration has been succesfully updated!
</body>
</html>"""

def post_config(environ,start_response):
   try:
      request_body_size = int(environ.get('CONTENT_LENGTH', 0))
   except (ValueError):
      print "no content length"
      request_body_size = 0
   request_body = environ['wsgi.input'].read(request_body_size)
   d = parse_qs(request_body)
   print d,request_body_size
   previous_url = escape(d.get('previous_url', ['http://www.google.com'])[0])
   jabber_id = escape(d.get('jabber_id', ['example@example.com'])[0])
   jabber_password = escape(d.get('jabber_password', ['xxx'])[0])

   storage.config["jabber_id"]=jabber_id
   storage.config["jabber_password"]=jabber_password
   storage.store()

   response_body=post_config_html % previous_url
   response_headers = [('Content-Type', 'text/html;charset=utf-8'),
                  ('Content-Length', str(len(response_body)))]
   start_response('200 OK', response_headers)
   return [response_body]
