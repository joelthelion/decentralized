#!/usr/bin/env python
import utils
from datamodel import *
import database as db
from utils import tokenize
from math import log,sqrt

def basic_similarity(l1,l2):
    w1,w2=tokenize(l1.title),tokenize(l2.title)
    return len(set(w1).intersection(w2))/float(len(w1+w2))

def better_similarity(l1,l2):
    w1,w2=tokenize(l1.title),tokenize(l2.title)
    return sum(len(w) for w in (set(w1).intersection(w2)))/log(len(w1+w2))

def freq_sim(l1,l2,freqz):
    w1,w2=tokenize(l1.title),tokenize(l2.title)
    return sum(1./log(freqz[w]) for w in (set(w1).intersection(w2)))/log(len(w1+w2))

def time_sim(l1,l2):
    return better_similarity(l1,l2)**2*1./sqrt((l1.date-l2.date).seconds+2)
    

def argmax(array,fn):
    return array[(max((fn(i),n) for n,i in enumerate(array)))[1]]

def frequencies(links):
    freqz={}
    for l in links:
        for w in tokenize(l.title):
            freqz[w]=freqz.get(w,0)+1
    return freqz

if __name__ == '__main__':
    import random
    s=db.Session()
    links=s.query(Link).all()
    initial=random.choice(links)
    freqz=frequencies(links)
    for func in [basic_similarity,better_similarity,lambda l1,l2:freq_sim(l1,l2,freqz),time_sim]:
        links=s.query(Link).all()
        selected=initial
        print "===================  ",func,"  ======================"
        for i in range(6):
            links.remove(selected)
            print selected.title.encode('utf-8')
            temp= argmax(links,lambda l:func(selected,l))
            #links.append(selected)
            selected=temp


    #for d in utils.most_frequent_duos(fwords):
    #    print d
