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
    for l in links:
        l.combined_prediction = \
                (sum( p.value * (accuracy[p.classifier]-0.5) for p in l.predictions if p.classifier!="idiot_class")/
                sum(accuracy[p.classifier]-0.5 for p in l.predictions if p.classifier!="idiot_class")) >= 0.
    s.commit()
    print "Done!"
