from mod_python import apache,util,Session
from web import sql
import time

def html_page(header,main,footer,title="kolmognus"):
    template="""<?xml version="1.0" encoding="UTF-8"?><!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en"><head><title>%s</title><link rel="stylesheet" href="/css/style.css"/></head><body><div class="header">%s</div><div class="main">%s</div><div class="footer">%s</div></body></html>"""
    return template % (title,header,main,footer)

def html_debug(param,request):
    template="""<div class="debug"><span class="key">parameters:</span> %s<br/><span class="key">uri:</span> %s<br/>generated in %.2fms</div>"""
    formatted_param=' '.join(param.keys())
    return template % (formatted_param,request.uri,1000*(time.time()-request.request_time))

def html_menu():
    menus=[
        ('/',"home"),
        ('/mp-info',"modpython")
    ]
    template="""<div class="menu"><a href="/"><img src="/image/logo.png" alt="KolmoGNUS"/></a><p>%s</p></div>"""
    menu_template="""<a href="%s">%s</a>"""
    return template % ' '.join([menu_template % (menu[0],menu[1].upper()) for menu in menus])

def html_session(param,request):
    template="""<div class="session">%s<p>%s</p></div>"""
    form_template="""<form action="" method="post"><input name="login" type="text" value="login"/><br/><input name="passwd" type="password" value="****"/><br/><input type="submit" value="go!!"/><input name="login_hidden" type="hidden"/></form>"""
    logged_template="""<p>Welcome %s!! <a href="?logout">logout</a></p>"""

    session=Session.Session(request,timeout=60)
    if param.has_key('logout'):
        session.invalidate()
        util.redirect(request,'/')
        return template % (form_template,'bye!!')
    if param.has_key('login_hidden') and param.has_key('login') and param.has_key('passwd'):
        login=param['login']
        passwd=param['passwd']
        if sql.request("select id from kolmognus_user where login='%s' and pass=PASSWORD('%s')" % (login,passwd)):
            session['login']=login
            session['hits']=0
            session.save()
            return template % (logged_template % session['login'],"%d hits" % session['hits'])
        else:
            return template % (form_template,"bad login")
    elif not session.is_new():
        session['hits']+=1
        session.save()
        return template % (logged_template % session['login'],"%d hits" % session['hits'])
    else:
        session.invalidate()
        return template % (form_template,"please login")
    
def html_users():
    template="""<div class="users"><h1>%d user(s):</h1><p>%s</p></div>"""
    users=sql.login_list()
    return template % (len(users)," ".join(users))

def html_feeds():
    template="""<div class="feeds"><h1>%d feed(s):</h1><p>%s</p></div>"""
    feed_template="""<a href="/feed/%s">%s</a> (%d hits)"""
    feeds=sql.request("select url_md5,url,hit_count from feed")
    return template % (len(feeds),"<br/>".join([feed_template % feed for feed in feeds]))

def html_stories():
    template="""<div class="stories"><h1>%d story(ies):</h1><p>%s</p></div>"""
    story_template="""<a href="/story/%s">%s</a> (%d hits) [%.50s]"""
    stories=sql.request("select url_md5,url,hit_count,symbols from story")
    return template % (len(stories),"<br/>".join([story_template % story for story in stories]))

def html_feed_info(feed_md5):
    template="""<div class="feed_info"><h1><a href="%s">%s</a></h1><p>fetched %d times, last fetching %s</p><h1>stories:</h1><p>%s</p></div>"""
    error_template="""<div class="feed_info"><h1>can't found feed info!!!</h1></div>"""
    story_template="""<a href="/story/%s">%s</a> (%d hits) [%.50s]"""

    feed=sql.request("select id,url,url,hit_count,fetch_date from feed where url_md5='%s'" % feed_md5)
    if feed:
        feed_id=feed[0][0]
        feed=feed[0][1:]
        stories=sql.request("select story.url_md5,story.url,story.hit_count,story.symbols\
            from story,feed_story where story.id=feed_story.story_id and feed_story.feed_id=%d" % feed_id)
        return template % (feed+("<br/>".join([story_template % story for story in stories]),))
    else:
        return error_template

def html_story_info(story_md5):
    template="""<div class="story_info"><h1><a href="%s">%s</a></h1><p>fetched %d times, last fetching %s</p><p>symbols: %s</p><h1>feeds:</h1><p>%s</p></div>"""
    error_template="""<div class="story_info"><h1>can't found story info!!!</h1></div>"""
    feed_template="""<a href="/feed/%s">%s</a> (%d hits)"""

    story=sql.request("select id,url,url,hit_count,fetch_date,symbols from story where url_md5='%s'" % story_md5)
    if story:
        story_id=story[0][0]
        story=story[0][1:]
        feeds=sql.request("select feed.url_md5,feed.url,feed.hit_count\
            from feed,feed_story where feed.id=feed_story.feed_id and feed_story.story_id=%d" % story_id)
        return template % (story+("<br/>".join([feed_template % feed for feed in feeds]),))
    else:
        return error_template

def handler(request):
    #request.content_type='text/plain'
    request.content_type='text/html'
    #request.discard_requestuest_body()
    request.send_http_header()

    param=util.FieldStorage(request,keep_blank_values=True)
    uri_param=request.uri.split('/')

    header=''
    header+=html_session(param,request)
    header+=html_menu()

    main_frame=''
    if len(uri_param)>2:
        if uri_param[1]=='feed':
            main_frame+=html_feed_info(uri_param[2])
        elif uri_param[1]=='story':
            main_frame+=html_story_info(uri_param[2])
        else:
            main_frame+="<h1>Crottei%s</h1>" % repr(uri_param)
    else:
        main_frame+=html_feeds()
        main_frame+=html_stories()
        main_frame+=html_users()

    footer=''
    footer+=html_debug(param,request)

    request.write(html_page(header,main_frame,footer).encode('utf-8'))
    return apache.OK
