#!/usr/bin/env python
import utils
from datamodel import *
import database as db

if __name__ == '__main__':
    s=db.Session()
    links=s.query(Link)
    total=0;good=0;bad=0;hidden=0
    for l in links:
        total+=1
        if l.evaluation:
            good+=1
        elif l.evaluation==False:
            bad+=1
        if l.hidden==True:
            hidden+=1
    print "%d links, %d good, %d bad, %d hidden" %(total,good,bad,hidden)
    frequent={}
    titles=[]
    for l in links:
        words=utils.tokenize(l.title)
        titles.append(words)
        for w in words:
            if frequent.has_key(w):
                frequent[w]+=1
            else:
                frequent[w]=1
    fwords=[w for w,f in frequent.items() if f>=4 and f<15]
    print fwords
    not_null=0
    for t in titles:
        for w in fwords:
            if w in t:
                not_null+=1
                break
    print float(not_null)/len(titles)*100.,len(fwords)
