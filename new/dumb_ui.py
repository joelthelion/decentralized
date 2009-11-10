#!/usr/bin/env python

if __name__ == "__main__":
    import database as db
    import time
    from datetime import datetime
    from datamodel import *
    s=db.Session()
    fresh = s.query(Link).filter(Link.evaluation == None).\
        order_by(Link.date.desc()).limit(10).all()
    for r in fresh:
        print "-",r
        print "Good, Bad, Hide? (g/b/h)"
        eval_dict={'g':1,'b':-1,'h':0}
        answer=eval_dict[raw_input().lower()]
        r.evaluation=answer
        r.evaluation_date=datetime.now()
        s.commit()
