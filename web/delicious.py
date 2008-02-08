#!/usr/bin/env python
#delicious content parser for sax xml parser implementation

import xml.sax.handler
import xml.sax
import sql
from urllib2 import HTTPError

#delicious feed parsing
def get_recent_stories():
    """Returns a list of recent URLs"""
    feed='http://delicious.com/rss/recent'
    return get_stories_for_feed(feed)

def get_stories_for_tag(tag):
    """Returns a list of URLs concerning a certain tag"""
    feed='http://delicious.com/rss/tag/%s' % tag
    return get_stories_for_feed(feed)

def get_stories_for_feed(feed):
    urls=get_valid_cached_stories_for_feed(feed)
    if not urls: #if cache invalid
        print "INFO: request for urls from feed '%s': fetching delicious" % feed
        urls=fetch_stories_for_feed(feed)
        update_feed_cache(feed,urls,change_date=True)
    else:
        print "INFO: request for urls from feed '%s': using cache" % feed
        update_feed_cache(feed,urls,change_date=False)
    return urls

def get_valid_cached_stories_for_feed(feed):
    rows=sql.request(u"select story.url from feed_story,feed,story\
                      where story.id=feed_story.story_id\
                        and feed_story.feed_id=feed.id\
                        and feed.url_md5=md5('%s')\
                        and addtime(feed.fetch_date,'00:30:00') >= now()" % feed)
    if rows:
        return [row[0] for row in rows]
    else:
        return []

def fetch_stories_for_feed(feed):
    handler=DeliciousTagHandler()
    try:
        xml.sax.parse(feed,handler)
        return handler.urls
    except HTTPError,e:
        print "ERROR: Could not retrieve delicious urls for feed '%s'" % feed
        print e
        return []

def update_feed_cache(feed,urls,change_date=False):
    sql.query("insert into feed (url,url_md5,fetch_date,hit_count) values ('%s',md5('%s'),now(),1)\
                    on duplicate key update hit_count=hit_count+1" % (feed,feed))
    if change_date:
        sql.query("update feed set fetch_date=now() where url_md5=md5('%s')"%feed)
        for url in urls:
            sql.query("insert into story (url,url_md5,hit_count) values ('%s',md5('%s'),0)\
              on duplicate key update id=id" % (url,url)) #nice hack
            sql.query("insert into feed_story (story_id,feed_id)\
              select story.id,feed.id\
              from story,feed\
              where story.url_md5=md5('%s')\
              and feed.url_md5=md5('%s')\
              on duplicate key update story_id=story_id" %(url,feed)) #nice hack II

class DeliciousURLHandler(xml.sax.handler.ContentHandler):
    """Parses a delicious rss of the form delicious/rss/url_md5"""
    def __init__(self):
        self.logins=[]
        self.tags=[]
        self.descriptions=[]
        self.authors=[]
        self.bookmark_dates=[]
        self.in_item=False
        self.in_description=False
        self.in_author=False
        self.in_tags=False
        self.in_bookmark_date=False
    def startElement(self,name,attributes):
        if name == "item":
            self.in_item=True
        elif name =="description":
            self.in_description=True
        elif name =="dc:subject":
            self.in_tags=True
        elif name =="dc:creator":
            self.in_author=True
        elif name =="dc:date":
            self.in_bookmark_date=True
    def characters(self, data):
        if self.in_item and data != "":
            if self.in_description: 
                self.descriptions.append(data)
            elif self.in_tags:
                self.tags.extend(data.split())
            elif self.in_author:
                self.authors.append(data)
            elif self.in_bookmark_date:
                self.bookmark_dates.append(data)
    def endElement(self,name):
        if name == "item":
            self.in_item=False
        elif name =="description":
            self.in_description=False
        elif name =="dc:subject":
            self.in_tags=False
        elif name =="dc:creator":
            self.in_author=False
        elif name =="dc:date":
            self.in_bookmark_date=False

#delicious story parsing
def get_symbols_for_story(url):
    symbols=get_valid_cached_symbols_for_story(url)
    if not symbols: #if cache invalid
        print "INFO: request for symbols from story '%s': fetching delicious" % url
        symbols=fetch_symbols_for_url(url)
        update_story_cache(url,symbols,change_date=True)
    else:
        print "INFO: request for symbols from story '%s': using cache" % url
        update_story_cache(url,symbols,change_date=False)
    return symbols

def update_story_cache(url,symbols,change_date=False):
    symbol_count=len(symbols.split(' '))
    sql.query("insert into story\
                 (url,url_md5,symbols,symbol_count,fetch_date,hit_count)\
                 values ('%s',md5('%s'),'%s',%d,now(),1)\
                 on duplicate key update hit_count=hit_count+1"%(url,url,symbols,symbol_count))
    if change_date:
        sql.query("update story set\
                     fetch_date=now() where\
                     url_md5=md5('%s')" % url)
        sql.query("update story set\
                     symbols='%s', symbol_count=%d where\
                     url_md5=md5('%s')"%(symbols,symbol_count,url))
    
def get_valid_cached_symbols_for_story(url):
    rows=sql.request("select symbols from story where\
                        url_md5=md5('%s')\
                        and addtime(fetch_date,'00:30:00') >= now()" % url)
    if rows:
        return rows[0][0]
    else: 
        return u""
    
def fetch_symbols_for_url(url):
    """Returns all the relevent delicious data concerning URL"""
    import md5,re
    del_format_url = url
    if not re.search(r"(.*//.*/.*\.|/$)",url): #try to format url according to delicious "norms"
        del_format_url+='/'
    feed='http://delicious.com/rss/url/%s' % md5.md5(del_format_url).hexdigest()
    handler=DeliciousURLHandler()
    try:
        xml.sax.parse(feed,handler)
        tags=list(set(handler.tags))
        import time
        pub_dates=[]
        for delicious_date_string in handler.bookmark_dates:
            try:
                pub_dates.append(time.mktime(time.strptime(delicious_date_string,"%Y-%m-%jT%H:%M:%SZ")))
            except ValueError:
                print "WARNING: unable to parse date string %s" % delicious_date_string
        try:
            pub_date = min(pub_dates)
        except ValueError:
            pub_date = time.time()
        return create_symbol_list(handler.authors,tags,handler.descriptions,pub_date)
    except HTTPError,e:
        print "WARNING: fetching symbols failed: ",e
        return create_symbol_list([],[],[],-1)

def create_symbol_list(authors,tags,descriptions,date):
    symbols = u' '.join(tags)
    if authors:
        symbols += ' '+' '.join(['liked_by_'+author for author in authors])
    return symbols
    
class DeliciousTagHandler(xml.sax.handler.ContentHandler):
    """Parses a delicious rss of the form delicious/rss/tag/c++"""
    def __init__(self):
        self.in_item=False
        self.urls=[]

    def startElement(self,name,attributes):
        if name=="item":
            self.urls.append(attributes["rdf:about"])
    def characters(self, data):
        pass
    def endElement(self,name):
        pass

if __name__=="__main__":
    
    print get_stories_for_tag("c++")
    print get_recent_stories()

