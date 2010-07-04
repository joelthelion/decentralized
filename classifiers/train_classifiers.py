#!/usr/bin/env python
import utils

if __name__ == '__main__':
    import classifiers
    from datamodel import *
    import database as db
    s=db.Session()
    evaluated=s.query(Link).filter(Link.evaluation != None).count()
    links=s.query(Link).filter(Link.evaluation != None).order_by(Link.date).all()[::2]
    print "Training on %d of %d evaluated links (every second element)" % (len(links),evaluated)
    for cl_name in utils.get_classifiers():
        current=__import__('classifiers.'+cl_name,fromlist=[classifiers])
        print "Training",cl_name
        current.train(links)
