#!/usr/bin/env python

import database as db
from sqlalchemy import Table, Column, Integer, String, Unicode,DateTime

class Link(db.Base):
    """A link is a potentially interesting URL, together with all the relevant metadata
    to help evaluate it"""
    __tablename__ = "links"
    url = Column(Unicode,primary_key=True)
    title = Column(Unicode)
    source = Column(Unicode)
    date = Column(DateTime)

    def __init__(self,u,t,s,d):
        self.url=u
        self.title=t
        self.source=s
        self.date=d

def get_links(rssfeed):
    from feedparser import parse
    import time
    from datetime import datetime
    f=parse(rssfeed)
    s=db.Session()
    for i in f.entries:
        s.merge(Link(unicode(i.link),unicode(i.title),unicode(f.url)\
            ,datetime.fromtimestamp(time.mktime(i.date_parsed))))
    s.commit()

if __name__ == '__main__':
    db.Base.metadata.create_all(db.engine)
    get_links("http://www.lemonde.fr/rss/une.xml")
