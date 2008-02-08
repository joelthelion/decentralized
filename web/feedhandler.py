from mod_python import apache,util
import sql
import common    

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

def html_feeds_info():
    template="""<div class="feeds_info"><h1>%d fetched feeds:</h1><p>%s</p><h1>%d never fetched feeds:</h1><p>%s</p></div>"""
    fetched_feed_template="""<a href="/feed/%s">%s</a> (%d hits)"""
    never_fetched_feed_template="""<a href="/feed/%s">%s</a>"""

    fetched_feed=sql.request("select url_md5,url,hit_count from feed where not isnull(fetch_date) order by hit_count asc")
    never_fetched_feed=sql.request("select url_md5,url from feed where isnull(fetch_date) order by id desc")
    return template % (len(fetched_feed),"<br/>".join([fetched_feed_template % feed for feed in fetched_feed])\
                      ,len(never_fetched_feed),"<br/>".join([never_fetched_feed_template % feed for feed in never_fetched_feed]))

def handler(request):
    request.content_type='text/html'
    request.send_http_header()

    param=util.FieldStorage(request,keep_blank_values=True)
    uri_param=request.uri.split('/')

    header=''
    header+=common.html_session(param,request)
    header+=common.html_menu()

    main_frame=''
    if len(uri_param)>2 and uri_param[1]=='feed':
	main_frame+=html_feed_info(uri_param[2])
    else:
        main_frame+=html_feeds_info()

    footer=''
    footer+=common.html_debug(param,request)

    request.write(common.html_page(header,main_frame,footer).encode('utf-8'))
    return apache.OK
