#!/usr/bin/env python

if __name__ == "__main__":
    import database as db
    import time
    import datetime
    from datamodel import *
    s=db.Session()
    old = s.query(Link).\
        filter(Link.evaluation == None).\
        filter(Link.date<datetime.datetime.fromtimestamp(time.time()-86400*2))
    for l in old:
        print "-",l
        s.delete(l)
    s.commit()
