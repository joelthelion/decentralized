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
    c_evals=evaluate_classifiers.test_classifiers()
    combination_func=adaboost_weight
    for method,eval in c_evals.items():
        print method,combination_func(eval.accuracy)
    for l in links:
        normal = sum(combination_func(c_evals[p.classifier].accuracy)\
                    for p in l.predictions if p.classifier!="idiot_class")
        assert( normal != 0)
        l.combined_prediction = \
                (sum( p.value * combination_func(c_evals[p.classifier].accuracy)\
                    for p in l.predictions if p.classifier!="idiot_class")/normal >= 0)
    s.commit()
    print "Done!"
