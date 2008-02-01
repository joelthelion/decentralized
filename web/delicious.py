#!/usr/bin/env python
#delicious content parser for sax xml parser implementation

import xml.sax.handler
import xml.sax
import md5
import sql
from urllib2 import HTTPError

#delicious urls parsing
def get_recent_urls():
    """Returns a list of recent URLs"""
    feed='http://delicious.com/rss/recent'
    return get_urls_for_feed(feed)

def get_urls_for_tag(tag):
    """Returns a list of URLs concerning a certain tag"""
    feed='http://delicious.com/rss/tag/%s' % tag
    return get_urls_for_feed(feed)

def get_urls_for_feed(feed):
    feed_md5=md5.md5(feed).hexdigest()
    urls=get_valid_cached_urls_for_feed(feed_md5)
    if not urls: #if cache invalid
        print "INFO: request for urls from feed '%s': fetching delicious" % feed
        urls=fetch_urls_for_feed(feed)
        update_urls_cache(feed_md5,urls,change_date=True)
    else:
        print "INFO: request for urls from feed '%s': using cache" % feed
        update_urls_cache(feed_md5,urls,change_date=False)
    return urls

def get_valid_cached_urls_for_feed(feed_md5):
    rows=sql.request("select urls from cached_url where url_md5='%s' and next_fetch >= now()" % feed_md5)
    if rows:
        return rows[0][0].split('|')
    else:
        return []

def fetch_urls_for_feed(feed):
    handler=DeliciousTagHandler()
    try:
        xml.sax.parse(feed,handler)
        return handler.urls
    except HTTPError,e:
        print "ERROR: Could not retrieve delicious urls for feed '%s'" % feed
        print e
        return []
    
def update_feed_count(feed_md5):
    """Increment the fetch count for a feed"""
    
def update_urls_cache(feed_md5,urls,change_date=False):
    rows=sql.request("select fetched_count from cached_url where url_md5='%s'" % feed_md5)
    if rows: #already in database
        if change_date:
            joined_urls='|'.join(urls)
            sql.query("update cached_url set fetched_count=fetched_count+1, urls='%s', next_fetch=addtime(now(),'00:30:00') where url_md5='%s'" % (joined_urls,feed_md5))
        else:
            sql.query("update cached_url set fetched_count=fetched_count+1 where url_md5='%s';" % feed_md5)
    else:
        joined_urls='|'.join(urls)
        sql.query("insert into cached_url (url_md5,next_fetch,urls,fetched_count) values ('%s',addtime(now(),'00:30:00'),'%s',1)" % (feed_md5,joined_urls))

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

#delicious tag parsing
def get_delicious_data_for_url(url):
    """Returns all the relevent delicious data concerning URL"""
    feed='http://delicious.com/rss/url/%s' % md5.md5(url).hexdigest()
    handler=DeliciousURLHandler()
    acquire_delicious()
    try:
        xml.sax.parse(feed,handler)
    except HTTPError,e:
        return ([],[],[],-1)
    tags=list(set(handler.tags))
    import time
    pub_dates=[]
    for delicious_date_string in handler.bookmark_dates:
        try:
            pub_dates.append(time.mktime(time.strptime(delicious_date_string,"%Y-%m-%jT%H:%M:%SZ")))
        except ValueError:
            print "WARNING: unable to parse date string %s" % delicious_date_string
    pub_date = min(pub_dates)
    return (handler.authors,tags,handler.descriptions,pub_date)
    
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
    
    print get_urls_for_tag("c++")
    print get_recent_urls()

    logins,tags,descriptions,date=get_delicious_data_for_url("http://www.lemonde.fr/")
    print descriptions
    print logins
    print tags
    print date
