#!/usr/bin/env python

from datamodel import Link,LinkSource

def get_links(rssfeed,session):
    from feedparser import parse
    import time
    from datetime import datetime
    f=parse(rssfeed)
    for i in f.entries:
        current_link=s.query(Link).filter_by(url=unicode(i.link)).first()
        if not current_link:
            if i.has_key("date_parsed"):
                current_link=Link(unicode(i.link),unicode(i.title),datetime.fromtimestamp(time.mktime(i.date_parsed)))
            else:
                #use the scrape date if the information isn't there
                current_link=Link(unicode(i.link),unicode(i.title),datetime.now()) 
        elif s.query(LinkSource).filter_by(link=current_link).filter_by(source=unicode(f.url)).first():
            continue # entry is already there
        current_link.sources.append(LinkSource(current_link.url,unicode(f.url)))
        session.merge(current_link)

if __name__ == '__main__':
    import database as db
    from utils import feeds

    db.Base.metadata.create_all(db.engine)

    s=db.Session()
    import sys
    for f in feeds:
        get_links(f,s)
        print ".",
        sys.stdout.flush()
    s.commit()
    print
    #get_links("file://une.xml")
    #import time
    #t=time.time()
    #for i in range(10000):
    #    get_links("file://une.xml")
    #print time.time()-t
