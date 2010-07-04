#!/usr/bin/env python

if __name__ == "__main__":
    import database as db
    import time
    import datetime
    from datamodel import *
    s=db.Session()
    recent = s.query(Link).all()
    print len(recent)
