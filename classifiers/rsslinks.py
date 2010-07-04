#!/usr/bin/env python

from datamodel import Link,LinkSource

def get_links(rssfeed):
    import database as db
    from feedparser import parse
    from datetime import datetime
    from time import time
    from random import random
    try:
        t=time()
        f=parse(rssfeed)
        session=db.Session()
        added=0
        for i in f.entries:
            current_link=session.query(Link).filter_by(url=unicode(i.link)).first()
            if not current_link:
                added+=1
                #can't trust the link date, it is dependent on RSS time fuse
                current_link=Link(unicode(i.link),unicode(i.title),\
                    datetime.fromtimestamp(time()+random()*30))
                session.add(current_link)
            elif unicode(f.url) in (s.source for s in current_link.sources):
                continue # entry is already there
            current_link.sources.append(LinkSource(current_link.url,unicode(f.url)))
        session.commit()
        print rssfeed,"(%.2fs)"%(time()-t)
        return added
    except Exception as e:
        print "Exception when parsing %s" % rssfeed
        print e
        return 0

if __name__ == '__main__':
    from utils import feeds
    import multiprocessing
    pool=multiprocessing.Pool(10)
    added=pool.map(get_links,feeds) #do 10 feeds at a time
    if sum(added) > 0:
        print "Added %d link(s) to the database!" % sum(added)
