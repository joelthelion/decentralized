#!/usr/bin/env python
#delicious content parser for sax xml parser implementation


import xml.sax.handler
import xml.sax
from urllib2 import HTTPError

last_delicious_fetch_date=-1
min_delicious_hammer_delay=3

def acquire_delicious():
    """Checks if we are not hammering delicious too much. If so, wait"""
    import time
    current=time.time()
    if current - globals()['last_delicious_fetch_date'] < globals()['min_delicious_hammer_delay']:
        print "Delicious hammer delay..."
        time.sleep(min_delicious_hammer_delay-(current-globals()['last_delicious_fetch_date']))
        print "Ok!"
    globals()['last_delicious_fetch_date']=time.time()

def get_recent_urls():
    """Returns a list of URLs concerning a certain tag"""
    feed='http://delicious.com/rss/recent'
    handler=DeliciousTagHandler()
    acquire_delicious()
    try:
        xml.sax.parse(feed,handler)
    except HTTPError,e:
        print "ERROR: Could not retrieve recent delicious urls"
        print e
        return []
    return handler.urls

def get_urls_for_tag(tag):
    """Returns a list of URLs concerning a certain tag"""
    feed='http://delicious.com/rss/tag/%s' % tag
    handler=DeliciousTagHandler()
    acquire_delicious()
    try:
        xml.sax.parse(feed,handler)
    except HTTPError:
        return []
    return handler.urls

def get_delicious_data_for_url(url):
    """Returns all the relevent delicious data concerning URL"""
    import md5
    feed='http://delicious.com/rss/url/%s' % md5.md5(url).hexdigest()
    handler=DeliciousURLHandler()
    acquire_delicious()
    try:
        xml.sax.parse(feed,handler)
    except HTTPError:
        return ([],[],[],-1)
    tags=list(set(handler.tags))
    import time
    pub_dates=[]
    for delicious_date_string in handler.bookmark_dates:
        try:
            pub_dates.append(time.mktime(time.strptime(delicious_date_string,"%Y-%m-%jT%H:%M:%SZ")))
        except ValueError:
            print "Warning : unable to parse date string %s" % delicious_date_string
    pub_date = min(pub_dates)
    return (handler.authors,tags,handler.descriptions,pub_date)
    
class DeliciousURLHandler(xml.sax.handler.ContentHandler):
    """Parses a delicious rss of the form delicious/rss/md5"""
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
