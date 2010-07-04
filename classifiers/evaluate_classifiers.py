#!/usr/bin/env python
import utils
from datamodel import *

class ClassifierEvaluation:
    def __init__(self,method_name):
        import classifiers
        import database as db
        from math import fabs
        self.method_name=method_name
        s=db.Session()
        links=s.query(Link).filter(Link.evaluation != None).order_by(Link.date).all()[1::2]
        if links:
            current=__import__('classifiers.'+method_name,fromlist=[classifiers])
            accuracy=0;confidence_weighted_ac=0
            cum_certainty=0
            fp,fn=0,0
            for l in links:
                prediction=current.predict(l)
                cum_certainty+=fabs(prediction)
                if ( prediction >= 0. ) == l.evaluation:
                    confidence_weighted_ac+=fabs(prediction)
                    accuracy+=1
                else:
                    confidence_weighted_ac-=fabs(prediction)
                    if (prediction >= 0): fp+=1
                    else: fn+=1
            test_size=len(links)
            self.accuracy=float(accuracy)/test_size
            self.confidence=float(confidence_weighted_ac)/test_size
            self.weighted_acc=float(confidence_weighted_ac)/cum_certainty
            self.false_positive_rate=float(fp)/test_size
            self.false_negative_rate=float(fn)/test_size
        else:
            self.accuracy=0.6
            self.weighted_acc=0
            self.confidence=0
            self.false_positive_rate=0
            self.false_negative_rate=0
    def __repr__(self):
        return "accuracy: %.4f\tconf.-weighted acc: %.4f\tconf.: %.4f\tfp: %.4f\tfn:%.4f" %\
                (self.accuracy,self.weighted_acc,self.confidence,\
                self.false_positive_rate,self.false_negative_rate)

def show_classifiers():
    import classifiers
    for cl_name in utils.get_classifiers():
        current=__import__('classifiers.'+cl_name,fromlist=[classifiers])
        print "- "+cl_name+":";current.print_self()

def test_classifiers():
    from math import fabs
    cl_evaluations={}
    for cl_name in utils.get_classifiers():
        cl_evaluations[cl_name]=ClassifierEvaluation(cl_name)
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
