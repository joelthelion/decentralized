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
            #can't trust the link date, it is dependent on RSS time fuse
            current_link=Link(unicode(i.link),unicode(i.title),datetime.now()) 
        elif unicode(f.url) in (s.source for s in current_link.sources):
            continue # entry is already there
        current_link.sources.append(LinkSource(current_link.url,unicode(f.url)))
        session.merge(current_link)

if __name__ == '__main__':
    import database as db
    from utils import feeds
    from time import time

    db.Base.metadata.create_all(db.engine)

    s=db.Session()
    for f in feeds:
        t=time()
        get_links(f,s)
        print f,"(%.2fs)"%(time()-t)
    s.commit()
    #get_links("file://une.xml")
    #import time
    #t=time.time()
    #for i in range(10000):
    #    get_links("file://une.xml")
    #print time.time()-t
