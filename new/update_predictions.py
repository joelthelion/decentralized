#!/usr/bin/env python


def get_classifiers():
    import re
    import os
    return [module[:-3] for module in os.listdir('classifiers') if re.search('_class\.py$',module)]


if __name__ == '__main__':
    import classifiers
    from datamodel import *
    import database as db
    s=db.Session()
    links=s.query(Link).order_by(Link.date.desc()).limit(15)
    for l in links:
        print l.title
        for cl_name in get_classifiers():
            current=__import__('classifiers.'+cl_name,fromlist=[classifiers])
            print cl_name,":",current.predict(l)
