#!/usr/bin/env python

import database as db
from sqlalchemy import Table, Column, Boolean, Integer, Unicode,DateTime,ForeignKey
from sqlalchemy.orm import relation,backref

class Link(db.Base):
    """A link is a potentially interesting URL, together with all the relevant metadata
    to help evaluate it"""
    __tablename__ = "links"
    url = Column(Unicode,primary_key=True)
    title = Column(Unicode)
    sources = relation("LinkSource",backref=backref('link'))
    date = Column(DateTime)
    """The two next columns are filled when the user evaluated the link"""
    evaluation = Column(Boolean)
    evaluation_date = Column(DateTime)

    def __init__(self,u,t,d):
        self.url=u
        self.title=t
        self.date=d
    def __repr__(self):
        return self.title.encode('utf-8')+\
            " ("+self.url.encode('utf-8')+")"

class LinkSource(db.Base):
    """The sources of a link. Can contain additional pieces of info
    only relevant to a certain source, such as points for a reddit link"""
    __tablename__ = "linksources"
    link_url = Column(Unicode,ForeignKey('links.url'),primary_key=True)
    """source is a source identifier, such as the URL of an RSS feed, or
    the jabber id of a friend"""
    source = Column(Unicode,primary_key=True)
    def __init__(self,l,s):
        self.link_url=l
        self.source=s
    def __repr__(self):
        return "link \"" + self.link_url.encode('utf-8')+"\" linked to by "+self.source.encode('utf-8')

def get_links(rssfeed):
    from feedparser import parse
    import time
    from datetime import datetime
    f=parse(rssfeed)
    s=db.Session()
    for i in f.entries:
        newlink=Link(unicode(i.link),unicode(i.title),datetime.fromtimestamp(time.mktime(i.date_parsed)))
        newlink.sources=[LinkSource(newlink.url,unicode(f.url))]
        s.merge(newlink)
    s.commit()

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    get_links("http://www.lemonde.fr/rss/une.xml")
    #get_links("file://une.xml")
    #import time
    #t=time.time()
    #for i in range(10000):
    #    get_links("file://une.xml")
    #print time.time()-t
