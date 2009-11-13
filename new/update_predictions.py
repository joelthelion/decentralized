#!/usr/bin/env python
import utils

if __name__ == '__main__':
    import classifiers
    from datamodel import *
    import database as db
    s=db.Session()
    print "Computing individual predictions..."
    links=s.query(Link).order_by(Link.date.desc())
    for cl_name in utils.get_classifiers():
        print cl_name
        current=__import__('classifiers.'+cl_name,fromlist=[classifiers])
        for l in links:
            s.merge(Prediction(l.url,unicode(cl_name),round(current.predict(l),2)))
    s.commit()

    print "Combining the classifications..."
    import evaluate_classifiers
    accuracy=evaluate_classifiers.test_classifiers()
    for l in links:
        l.combined_prediction = \
                (sum( p.value * accuracy[p.classifier] for p in l.predictions)/
                sum(accuracy[p.classifier] for p in l.predictions)) >= 0.
    s.commit()
    print "Done!"
