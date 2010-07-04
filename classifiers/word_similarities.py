#!/usr/bin/env python
import utils

def compute_sims(link,ws):
    words=utils.tokenize(link.title)
    for w in words:
        for w2 in words:
            if w != w2:
                pair=frozenset((w,w2))
                assert(len(list(pair))>1)
                ws[pair]=ws.get(pair,0)+1
    return word_similarities
        
def compute_freq_sims(link,ws,freqz):
    from math import sqrt
    words=utils.tokenize(link.title)
    for w in words:
        for w2 in words:
            if w != w2:
                pair=frozenset((w,w2))
                ws[pair]=ws.get(pair,0)+1./(freqz[w]+freqz[w2]+15)
    return word_similarities

if __name__ == '__main__':
    import database as db
    from datamodel import *
    s=db.Session()
    links=s.query(Link).all()
    word_similarities={}
    freqz=utils.word_frequencies(links)
    for l in links:
        word_similarities=compute_freq_sims(l,word_similarities,freqz)
    a=[(tuple(s),f) for s,f in word_similarities.items()]
    a.sort(key=lambda i:i[1])
    for (w1,w2),f in a[-100:]:
        print w1,w2,"%.2f"%f
