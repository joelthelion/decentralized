#!/usr/bin/env python

if __name__ == "__main__":
    import database as db
    import time
    import datetime
    from datamodel import *
    s=db.Session()
    recent = s.query(Link).filter(Link.date>datetime.datetime.fromtimestamp(time.time()-3600)).\
        order_by(Link.date.desc()).limit(10).all()
    recent.reverse()
    for r in recent:
        print r
