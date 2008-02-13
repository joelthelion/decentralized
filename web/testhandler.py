from mod_python import apache,util
from xml.sax import saxutils
import sql
import common    

def html_users():
    template="""<div class="users"><h1>%d user(s):</h1><p>%s</p></div>"""
    users=sql.login_list()
    return template % (len(users)," ".join(users))

def html_feeds():
    template="""<div class="feeds"><h1>recent feeds:</h1><p>%s</p></div>"""
    feed_template="""<a href="/feed/%s">%s</a> (%d hits)"""
    feeds=sql.request("select url_md5,url,hit_count from feed order by fetch_date asc limit 10")
    return template % "<br/>".join([feed_template % feed for feed in feeds])

def html_stories():
    template="""<div class="stories"><h1>recent stories:</h1><p>%s</p></div>"""
    story_template="""<a href="/story/%s">%.50s</a> %d hits, %d symbols [%.50s]"""
    stories=sql.request("select url_md5,url,hit_count,symbol_count,symbols from story where not isnull(symbol_count) and not symbol_count=0 order by fetch_date asc limit 10")
    return template % "<br/>".join([story_template % (story[0],saxutils.escape(story[1]),story[2],story[3],saxutils.escape(story[4])) for story in stories])

def html_recommended_stories(session):
    template="""<div class="recommended_stories"><h1>recommended stories:</h1><p>%s</p></div>"""
    recommended_story_template="""<form method="post" action=""><a href="/story/%s">%.50s</a> <span class="rating">%.2f</span> <a href="%s" class="view_it">view it</a> <input type="button" class="good" value="good"/> <input type="button" class="bad" value="bad"/></form>"""
    recommended_stories=sql.request("select story.url_md5, story.url, recommended_story.computed_rating from story, recommended_story, kolmognus_user\
        where recommended_story.user_id=kolmognus_user.id and recommended_story.story_id=story.id\
        and kolmognus_user.login=%s and recommended_story.user_rating='?'\
        order by recommended_story.computed_rating desc",session['login'])
    return template % "<br/>".join([recommended_story_template % (story[0],saxutils.escape(story[1]),story[2],saxutils.escape(story[1])) for story in recommended_stories])

def handler(request):
    welcome="""<div class="welcome"><p>Welcome to KolmoGNUS, the bayesian classifier that finds cool links for YOU</p></div>"""
    param,session=common.init_request(request)

    header=''
    header+=common.html_session(param,session,request)
    header+=common.html_menu()

    main_frame=''
    if session.has_key('login'): #user logged in
        main_frame+=html_recommended_stories(session)
    else:
        main_frame+=welcome
    main_frame+=html_feeds()
    main_frame+=html_stories()
    main_frame+=html_users()

    footer=''
    footer+=common.html_debug(param,request)

    request.write(common.html_page(header,main_frame,footer).encode('utf-8'))
    return apache.OK
