#!/usr/bin/env python
import utils

if __name__ == '__main__':
    import classifiers
    from datamodel import *
    import database as db
    s=db.Session()
    links=s.query(Link).order_by(Link.date.desc()).limit(15)
    for l in links:
        print l.title
        for cl_name in utils.get_classifiers():
            current=__import__('classifiers.'+cl_name,fromlist=[classifiers])
            print cl_name,":",current.predict(l)
