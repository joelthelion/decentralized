#!/usr/bin/env python
import utils
from datamodel import *

def show_classifiers():
    import classifiers
    for cl_name in utils.get_classifiers():
        current=__import__('classifiers.'+cl_name,fromlist=[classifiers])
        print "- "+cl_name+":";current.print_self()

def test_classifiers():
    import classifiers
    import database as db
    from math import fabs
    s=db.Session()
    links=s.query(Link).filter(Link.evaluation != None).order_by(Link.date.desc()).all()[1::2]
    accuracy,confidence_weighted_ac={},{}
    for cl_name in utils.get_classifiers():
        current=__import__('classifiers.'+cl_name,fromlist=[classifiers])
        accuracy[cl_name]=0;confidence_weighted_ac[cl_name]=0
        for l in links:
            prediction=current.predict(l)
            if ( prediction >= 0. ) == l.evaluation:
                confidence_weighted_ac[cl_name]+=fabs(prediction)
                accuracy[cl_name]+=1
            else:
                confidence_weighted_ac[cl_name]-=fabs(prediction)
    for dic in accuracy,confidence_weighted_ac:
        for k in dic.keys():
            dic[k]=float(dic[k])/len(links)
    return (accuracy,confidence_weighted_ac)

if __name__ == '__main__':
    show_classifiers()
    acc,conf=test_classifiers()
    print "Global results:"
    print
    for method in acc.keys():
        print method,": %.4f (accuracy), %.4f (confidence_weighted) "% (acc[method],conf[method])
    s=db.Session()
    evaluated=s.query(Link).filter(Link.evaluation != None).count()
    links=s.query(Link).filter(Link.evaluation != None).order_by(Link.date.desc()).all()[1::2]
    print "Evaluating on %d of %d evaluated links (every other element)" % (len(links),evaluated)
    print "Global accuracy: %.4f" % (float(sum(1-abs(l.combined_prediction - l.evaluation)\
        for l in links)) / len(links))
