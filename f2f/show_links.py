from daemon import my_posts

show_links_html= """
<html>
<title>Your latest posts</title>
<body>
<h2> Your latest posts</h2>
%s
</body>
</html>"""

def show_link(url,title):
    return """<p><a href="%s">%s</a></p>""" % (url,title)

def show_links(environ,start_response):
 
    html="""<div class=html>"""
    for p in my_posts:
    	html+=show_link(p.url,p.title)
    html+="</div>"
    response_body=show_links_html % html
    response_headers = [('Content-Type', 'text/html;charset=utf-8'),
                   ('Content-Length', str(len(response_body)))]
    start_response('200 OK', response_headers)
    return [response_body]
