#!/usr/bin/env python

from sqlalchemy.orm import sessionmaker
Session=sessionmaker()

from sqlalchemy.ext.declarative import declarative_base
Base=declarative_base()
from sqlalchemy import Table, Column, Integer, String, Unicode,DateTime

class Link(Base):
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
    s=Session()
    for i in f.entries:
        s.merge(Link(unicode(i.link),unicode(i.title),unicode(f.url)\
            ,datetime.fromtimestamp(time.mktime(i.date_parsed))))
    s.commit()

if __name__ == '__main__':
    from sqlalchemy import create_engine
    engine=create_engine("sqlite:///test.db")
    Session.configure(bind=engine)
    Base.metadata.create_all(engine)

    get_links("http://www.lemonde.fr/rss/une.xml")
