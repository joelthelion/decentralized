from mod_python import apache,util
from xml.sax import saxutils
import sql
import common    

def html_story_info(story_md5):
    template="""<div class="story_info"><h1><a href="%s">%.100s</a></h1><p>fetched %d times, contains %d symbols, last fetching %s</p><p>symbols: %s</p><h1>found in feeds:</h1><p>%s</p></div>"""
    error_template="""<div class="story_info"><h1>can't found story info!!!</h1></div>"""
    feed_template="""<a href="/feed/%s">%s</a> (%d hits)"""

    story=sql.request("select id,url,url,hit_count,symbol_count,fetch_date,symbols from story where url_md5=%s" , story_md5)
    if story:
        story_id=story[0][0]
        story=story[0][1:]
        feeds=sql.request("select feed.url_md5,feed.url,feed.hit_count from feed,feed_story where feed.id=feed_story.feed_id and feed_story.story_id=%s" , int(story_id))
        return template % (saxutils.escape(story[0]),saxutils.escape(story[1]),story[2],story[3],story[4],saxutils.escape(story[5]),"<br/>".join([feed_template % feed for feed in feeds]))
    else:
        return error_template

def html_stories_info():
    template="""<div class="stories_info"><h1>%d fetched stories:</h1><p>%s</p><h1>%d never fetched stories:</h1><p>%s</p><h1>%d no symbol stories:</h1><p>%s</p></div>"""
    fetched_story_template="""<a href="/story/%s">%s</a> (%d hits, %d symbols)"""
    never_fetched_story_template="""<a href="/story/%s">%s</a>"""
    no_symbol_story_template="""%s"""

    fetched_story=sql.request("select url_md5,url,hit_count,symbol_count from story where not isnull(fetch_date) and not isnull(symbols) order by symbol_count desc")
    never_fetched_story=sql.request("select url_md5,url from story where isnull(fetch_date) order by id desc")
    no_symbol_story=sql.request("select url from story where isnull(symbols) order by id desc")
    return template % (len(fetched_story),"<br/>".join([fetched_story_template % (story[0], saxutils.escape(story[1]), story[2], story[3]) for story in fetched_story])\
                      ,len(never_fetched_story),"<br/>".join([never_fetched_story_template % (story[0], saxutils.escape(story[1])) for story in never_fetched_story])\
                      ,len(no_symbol_story),"<br/>".join([no_symbol_story_template % saxutils.escape(story[0]) for story in no_symbol_story]))

def handler(request):
    request.content_type='application/xhtml+xml'
    #request.content_type='text/html'
    #request.discard_requestuest_body()
    request.send_http_header()

    param=common.decode_param_strings(util.FieldStorage(request,keep_blank_values=True))
    uri_param=request.uri.split('/')

    header=''
    header+=common.html_session(param,request)
    header+=common.html_menu()

    main_frame=''
    if len(uri_param)>2 and uri_param[1]=='story':
	main_frame+=html_story_info(uri_param[2])
    else:
        main_frame+=html_stories_info()

    footer=''
    footer+=common.html_debug(param,request)

    request.write(common.html_page(header,main_frame,footer).encode('utf-8'))
    return apache.OK
