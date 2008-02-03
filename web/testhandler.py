from mod_python import apache,util
from web import sql
import time

def html_page(body,title="kolmognus"):
    template="""<html><head><title>%s</title><link rel="stylesheet" href="/css/style.css"/></head><body>%s</body></html>"""
    return template % (title,body)

def html_debug(request):
    template="""<div class="debug"><span class="key">parameters:</span> %s<br/><span class="key">uri:</span> %s<br/>generated in %.2fms</div>"""
    param=util.FieldStorage(request,keep_blank_values=True)
    formatted_param=' '.join(['%s=%s' % (field.name,field.value) if field.value else field.name for dummy,field in param.items()])
    return template % (formatted_param,request.uri,1000*(time.time()-request.request_time))

def html_users(request):
    template="""<div class="users"><h1>%d user(s):</h1><p>%s<p></div>"""
    users=sql.login_list()
    return template % (len(users)," ".join(users))

def html_feeds(request):
    template="""<div class="feeds"><h1>%d feed(s):</h1><p>%s</p></div>"""
    feed_template="""<a href="/feed/%s">%s</a> (%d hits)"""
    feeds=sql.request("select url_md5,url,hit_count from feed")
    return template % (len(feeds),"<br/>".join([feed_template % feed for feed in feeds]))

def html_stories(request):
    template="""<div class="stories"><h1>%d story(ies):</h1><p>%s</p></div>"""
    story_template="""<a href="/story/%s">%s</a> (%d hits)"""
    stories=sql.request("select url_md5,url,hit_count from story")
    return template % (len(stories),"<br/>".join([story_template % story for story in stories]))

def handler(request):
    #request.content_type='text/plain'
    request.content_type='text/html'
    #request.discard_requestuest_body()
    request.send_http_header()

    body=''
    body+=html_feeds(request)
    body+=html_stories(request)
    body+=html_users(request)
    body+=html_debug(request)

    request.write(html_page(body))
    return apache.OK
