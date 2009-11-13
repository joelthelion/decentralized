#!/usr/bin/env python
import utils
from datamodel import *

def test_classifiers():
    import classifiers
    import database as db
    from math import fabs
    s=db.Session()
    links=s.query(Link).filter(Link.evaluation != None).order_by(Link.date.desc()).limit(100).all()
    results={}
    for cl_name in utils.get_classifiers():
        current=__import__('classifiers.'+cl_name,fromlist=[classifiers])
        print "- "+cl_name+":";current.print_self()
        results[cl_name]=0
        for l in links:
            prediction=current.predict(l)
            if ( prediction >= 0. ) == l.evaluation:
                results[cl_name]+=fabs(prediction)
            else:
                results[cl_name]-=fabs(prediction)
    for k in results.keys():
        results[k]=float(results[k])/len(links)
    return results

if __name__ == '__main__':
    results=test_classifiers()
    for method in results.keys():
        print method,": %.4f"%results[method]
    s=db.Session()
    links=s.query(Link).filter(Link.evaluation != None).order_by(Link.date.desc()).limit(100).all()
    print "Global accuracy: %.4f" % (float(sum(1-abs(l.combined_prediction - l.evaluation)\
        for l in links)) / len(links))
