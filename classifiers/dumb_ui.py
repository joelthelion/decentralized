#!/usr/bin/env python

def evaluate(link,session):
    print "-",link
    print "Good, Bad, Hide? (g/b/h)"
    answer=raw_input().lower()
    if answer == 'g':
        link.evaluation=True
    elif answer == 'b':
        link.evaluation=False
    elif answer == 'h' or answer =='':
        link.hidden=True
    else:
        print "I didn't understand..."
        evaluate(link,session)
    link.evaluation_date=datetime.now()
    s.commit()


if __name__ == "__main__":
    import database as db
    import time
    from datetime import datetime
    from datamodel import *
    s=db.Session()
    fresh = s.query(Link).filter(Link.evaluation_date == None).\
        filter_by(combined_prediction=True).\
        order_by(Link.date.desc()).limit(10).all()
    for r in fresh:
        evaluate(r,s)
