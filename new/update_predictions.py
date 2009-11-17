#!/usr/bin/env python
import utils
from sqlalchemy import or_

def naive_weight(accuracy):
    return accuracy-0.5

def adaboost_weight(accuracy):
    from math import log
    return 0.5*log(accuracy/(1-accuracy))

if __name__ == '__main__':
    import classifiers
    from datamodel import *
    import database as db
    from datetime import datetime
    from time import time
    s=db.Session()
    print "Computing individual predictions..."
    #evaluate rated stories and recent ones
    links=s.query(Link).\
        filter(or_(\
            Link.evaluation != None,\
            Link.date > datetime.fromtimestamp(time()-86400)))
    for cl_name in utils.get_classifiers():
        print cl_name
        current=__import__('classifiers.'+cl_name,fromlist=[classifiers])
        for l in links:
            found=False
            for p in l.predictions:
                if p.link_url == l.url and p.classifier == unicode(cl_name):
                    p.value=round(current.predict(l),2)
                    found=True
                    break
            if not found:
                l.predictions.append(Prediction(l.url,unicode(cl_name),round(current.predict(l),2)))
        s.commit()

    print "Combining the classifications..."
    import evaluate_classifiers
    accuracy,conf_weighted=evaluate_classifiers.test_classifiers()
    combination_func=adaboost_weight
    for c,a in accuracy.items():
        print c,combination_func(a)
    for l in links:
        l.combined_prediction = \
                (sum( p.value * combination_func(accuracy[p.classifier]) for p in l.predictions if p.classifier!="idiot_class")/
                sum(combination_func(accuracy[p.classifier]) for p in l.predictions if p.classifier!="idiot_class")) >= 0.
    s.commit()
    print "Done!"
