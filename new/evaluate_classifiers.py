#!/usr/bin/env python
import utils
from datamodel import *

class ClassifierEvaluation:
    def __init__(self,accuracy,confidence,false_positives,false_negatives,test_size):
        if test_size:
            self.accuracy=float(accuracy)/test_size
            self.confidence=float(confidence)/test_size
            self.false_positive_rate=float(false_positives)/test_size
            self.false_negative_rate=float(false_negatives)/test_size
        else:
            self.accuracy=0.6
            self.confidence=0
            self.false_positive_rate=0
            self.false_negative_rate=0
    def __repr__(self):
        return "accuracy: %.4f\tconfidence: %.4f\tfp: %.4f\tfn:%.4f" %\
            (self.accuracy,self.confidence,self.false_positive_rate,self.false_negative_rate)

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
    links=s.query(Link).filter(Link.evaluation != None).order_by(Link.date).all()[1::2]
    cl_evaluations={}
    for cl_name in utils.get_classifiers():
        current=__import__('classifiers.'+cl_name,fromlist=[classifiers])
        accuracy=0;confidence_weighted_ac=0
        fp,fn=0,0
        for l in links:
            prediction=current.predict(l)
            if ( prediction >= 0. ) == l.evaluation:
                confidence_weighted_ac+=fabs(prediction)
                accuracy+=1
            else:
                confidence_weighted_ac-=fabs(prediction)
                if (prediction >= 0): fp+=1
                else: fn+=1
        cl_evaluations[cl_name]=ClassifierEvaluation(accuracy,\
            confidence_weighted_ac,fp,fn,len(links))
    return cl_evaluations

if __name__ == '__main__':
    show_classifiers()
    evals=test_classifiers()
    print "Global results:"
    print
    for method,eval in evals.items():
        print method,eval
    s=db.Session()
    evaluated=s.query(Link).filter(Link.evaluation != None).count()
    links=s.query(Link).filter(Link.evaluation != None).order_by(Link.date).all()[1::2]
    print "Evaluating on %d of %d evaluated links (every other element)" % (len(links),evaluated)
    print "Global accuracy: %.4f" % (float(sum(1-abs(l.combined_prediction - l.evaluation)\
        for l in links)) / len(links))
