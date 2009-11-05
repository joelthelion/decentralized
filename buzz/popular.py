#!/usr/bin/env python
#Identify the latest trends on delicious

import os
import re
import cPickle

if __name__=='__main__':
    try:
        f=open(os.path.expanduser("~/.delicious_popular.pck"))
        latest,already_seen=cPickle.load(f)
        f.close()
    except IOError,e:
        print e
        print "delicious_popular file not found, creating a new one..."
        latest,already_seen=[],set()
    print "Fetching data from delicious..."
    os.system("""wget http://del.icio.us/tag/?sort=freq""")
    print "----------------------------------------------------------------------------------"
    print
    print
    current=[]
    for l in (l for l in open("index.html?sort=freq").readlines() if re.match(".*href=\"/tag/[^\"].*",l)):
        match=re.search("href=\"/tag/([^\"]*)",l)
        if match: current.append(match.groups()[0])
    current.reverse()
    disp_flag=False
    for popular in (c for c in current if c not in already_seen):
        if not disp_flag:
            print "Adding new buzzwords",
            disp_flag=True
        latest.append(popular)
        already_seen.add(popular)
        if len(latest)>30:
            latest.pop(0)
        print ".",
    if disp_flag:
        print 
    print "Latest buzzwords on delicious: (oldest to newest)"
    print " ".join(latest)
    f=open(os.path.expanduser("~/.delicious_popular.pck"),"wb")
    cPickle.dump((latest,already_seen),f,-1)
    f.close()
    os.system("rm index.html?sort=freq")
