#!/usr/bin/env python
# coding=utf8
#Identify the latest trends on delicious
from __future__ import division
import os
import re
import cPickle
import time
import sys

my_reddits="programming,technology,linux,xkcd,productivity,Health,newreddits,Physics,c_language,science,business,worldnews,math,Python,startups,bioinformatics,meta,smart,shell".split(",")

def tokenize(text):
    text=re.sub(u"""[/1234567890=@\-#…«»”“’‘.!"'()*,:;<>?\[\]`{|}~&]"""," ",text).lower()
    return text.split()
    
def add(dict,key):
    dict[key]=dict.get(key,0)+1

def add_tuple(dict,key,default_value,index=0):
    values=list(dict.get(key,default_value))
    values[index]+=1
    #print "add_tuple test: ",key.encode("utf-8"),values
    dict[key]=tuple(values)

def get_feed_stories(feeds=["http://digg.com/rss/index.xml","http://reddit.com/r/all/.rss","http://www.lemonde.fr/rss/sequence/0,2-3208,1-0,0.xml","http://linuxfr.org/backend/news-homepage/rss20.rss","http://del.icio.us/rss/","http://www.lefigaro.fr/rss/figaro_actualites.xml","http://news.ycombinator.com/rss","http://linuxfr.org/backend/journaux/rss20.rss","http://www.lepoint.fr/content/system/rss/a_la_une/a_la_une_doc.xml","http://rss.feedsportal.com/c/568/f/7295/index.rss","http://www.marianne2.fr/xml/syndication.rss","http://syndication.lesechos.fr/rss/rss_une.xml","http://blogs.lexpress.fr/attali/index.xml","http://feeds.feedburner.com/consommateur-si-tu-savais","http://www.reddit.com/r/AskReddit/","http://tempsreel.nouvelobs.com/file/rss_perm/rss_permanent.xml","http://top25.sciencedirect.com/rss.php?subject_area_id=17&journal_id=13618415","http://rss.sciencedirect.com/getMessage?registrationId=IHHEIIHEJNHFQHIGKHHLIMJFJLKKLLKJNZJMLPOLMN","http://feedproxy.google.com/Phoronix","http://rss.feedsportal.com/c/499/f/413823/index.rss","http://www.slate.fr/rss.xml"]):
    # disabled: "http://www.liberation.fr/interactif/rss/actualites/",
    import feedparser
    import time
    import random
    import sys
    stories=[]
    for r in my_reddits:
        feeds.append("http://reddit.com/r/%s/.rss"%r)
    #for f in random.sample(feeds,2):
    for f in feeds:
        print >>sys.stderr, "Fetching %s..." % f
        try:
            stories.extend((time.asctime().replace(" ",""),f,entry.title.encode('utf8')) for entry in feedparser.parse(f).entries)
        except:
            print "Error parsing %s..." % f
    return stories

def read_from_file(filename):
    stories=[]
    try:
        for l in open(filename).readlines():
            a=l.split(" ")
            stories.append((a[1]," ".join(a[2:])[:-1]))
    except IOError:
        import sys
        print >>sys.stderr,"Warning: Error while reading old stories file"
        return []
    return stories



if __name__=='__main__':
    from sys import argv,exit
    stories=get_feed_stories()
    old=read_from_file("toto.txt")
    
    for time,feed,title in stories:
        if (feed,title) not in old:
            print "%s %s %s" % (time,feed,title)
