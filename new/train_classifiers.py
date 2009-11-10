#!/usr/bin/env python
import utils

if __name__ == '__main__':
    import classifiers
    from datamodel import *
    import database as db
    s=db.Session()
    links=s.query(Link).filter(Link.evaluation != None)
    for cl_name in utils.get_classifiers():
        current=__import__('classifiers.'+cl_name,fromlist=[classifiers])
        print "Training",cl_name
        current.train(links)
