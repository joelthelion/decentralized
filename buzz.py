#!/usr/bin/env python
# coding=utf8
#Identify the latest trends on delicious
from __future__ import division
import os
import re
import cPickle
import time
import sys

MAXIMUM_TOTAL_WEIGHT=10000 #Maximum number of word counts. After, apply geometric decay
REPEAT_INTERVAL_DAYS=15 #Minimum number of days without seing a word required to count it as original again
FOCUS_DAYS=1 #Number of days a word stays interesting
my_reddits="programming,technology,linux,xkcd,productivity,Health,newreddits,Physics,c_language,science,business,worldnews,math,Python,startups,bioinformatics,meta,smart,shell".split(",")

def tokenize(text):
    text=re.sub(u"""[/1234567890@\-#…«»”“’‘.!"'()*,:;<>?\[\]`{|}~&]"""," ",text).lower()
    return text.split()
    
def add(dict,key):
    dict[key]=dict.get(key,0)+1

def add_tuple(dict,key,default_value,index=0):
    values=list(dict.get(key,default_value))
    values[index]+=1
    dict[key]=tuple(values)

def get_feed_stories(feeds=["http://digg.com/rss/index.xml","http://reddit.com/r/all/.rss","http://www.lemonde.fr/rss/sequence/0,2-3208,1-0,0.xml","http://linuxfr.org/backend/news-homepage/rss20.rss","http://del.icio.us/rss/","http://www.lefigaro.fr/rss/figaro_actualites.xml","http://www.liberation.fr/interactif/rss/actualites/","http://news.ycombinator.com/rss","http://linuxfr.org/backend/journaux/rss20.rss","http://feeds.feedburner.com/SteveOnImageProcessing"]):
    import feedparser
    stories=[]
    for r in my_reddits:
        feeds.append("http://reddit.com/r/%s/.rss"%r)
    for f in feeds:
        print "Fetching %s..." % f
        stories.extend((entry.title,f) for entry in feedparser.parse(f).entries)
    return stories

def get_object_from_file(filename,default={}):
    try:
        f=open(filename)
        mydict=cPickle.load(f)
        f.close()
    except IOError,e:
        print "%s file not found, creating a new one..." %filename
        mydict=default
    return mydict

def downsize_counts(already_seen):
    """Keeps word counts reasonable using geometric decay, so that new trends don't go unnoticed"""
    total=sum(count for now,count in already_seen.values())
    if total>MAXIMUM_TOTAL_WEIGHT*1.01: #*1.01 so we don't do it every time
        print "Total count too big (%d), downsizing counts..." % total
        for k,(now,old_count) in already_seen.items():
            already_seen[k]=now,old_count/(total/MAXIMUM_TOTAL_WEIGHT)

def show_original_stuff():
    now=time.time()
    import datetime
    today=datetime.date.fromtimestamp(now).toordinal()
    already_seen,distinct_use_days,last_use_day,todays_words=get_object_from_file(os.path.expanduser("~/.popurls_alreadyseen.pck"),({},0,0,{}))
    downsize_counts(already_seen)
    already_seen_links=get_object_from_file(os.path.expanduser("~/.popurls_alreadyseen_links.pck"),set())
    time_fetched,story_ratings=get_object_from_file(os.path.expanduser("~/.popurls.pck"),(0,None))

    if story_ratings is None or now-time_fetched>10 * 60: #if file is older than ten minutes
        common=set(unicode(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"common.txt")).read()[:-1],"utf8").split(","))
        all_stories=get_feed_stories()
        stories=[]
        for s,feed in all_stories:
            if s not in already_seen_links:
                already_seen_links.add(s)
                stories.append((s,feed))
        raw_text=" ".join(s for s,f in stories)
        if not stories: 
            print "No new stories found"
            import sys
            sys.exit()
        for word,(count,time_added) in todays_words.items():
            if now-time_added > 86400 * FOCUS_DAYS:
                del todays_words[word]
        if today > last_use_day:
            distinct_use_days+=1
        time_fetched=now
        for word in tokenize(raw_text):
            if word not in common and len(word)>=2:#Common words don't interest us
                if word in already_seen:
                    if word in todays_words:
                        add_tuple(todays_words,word,default_value=(0,now),index=1)
                    already_seen[word]=distinct_use_days,already_seen[word][1]+1 #this word is still being seen
                else:
                    already_seen[word]=distinct_use_days,1
                    add_tuple(todays_words,word,default_value=(0,now),index=1)
        #compute rated stories
        story_ratings=[ (story,int(100*sum(todays_words[w][0] for w in story_words \
                        if w in todays_words)/len(story_words)),feed)\
                for story,story_words,feed in ((s,tokenize(s),feed) for s,feed in stories)]
        story_ratings.sort(key=lambda e:e[1])

    for k,(t,dummy) in already_seen.items(): #If a keyword hasn't been seen in a month, it's interesting again
        if distinct_use_days-t>REPEAT_INTERVAL_DAYS:
            print ("Cleanup: removed %s from seen dictionnary" % k).encode('utf-8')
            del already_seen[k]
    print "Eliminated %d unoriginal stories" % sum(1 for s,rating,feed in story_ratings if rating==0)
    print "The most original stories are:"
    for s,rating,feed in story_ratings:
        if rating>0:
            print ("(%d) %s (%s)"%(rating,s,feed)).encode('utf-8')
    f=open(os.path.expanduser("~/.popurls_alreadyseen.pck"),"wb")
    cPickle.dump((already_seen,distinct_use_days,today,todays_words),f,-1)
    f.close()
    f=open(os.path.expanduser("~/.popurls.pck"),"wb")
    cPickle.dump((time_fetched,story_ratings),f,-1)
    f.close()
    f=open(os.path.expanduser("~/.popurls_alreadyseen_links.pck"),"wb")
    cPickle.dump(already_seen_links,f,-1)
    f.close()

def show_popular_words():
    import cPickle
    import os
    common=set(unicode(open(os.path.join(os.path.dirname(os.path.realpath(__file__)),"common.txt")).read()[:-1],"utf8").split(","))
    a,dummy1,dummy2,dummy3=cPickle.load(open(os.path.expanduser("~/.popurls_alreadyseen.pck")))
    a=a.items()
    a.sort(key=lambda e:e[1][1])
    for k in a:
        if k[0] not in common and k[1][1]>1: print ("%s (%.1f)"%(k[0],k[1][1])).encode('utf-8')
    print "There are %d words in the popular database" % len(a)

def show_todays_words():
    import time
    already_seen,distinct_use_days,last_use_day,todays_words=get_object_from_file(os.path.expanduser("~/.popurls_alreadyseen.pck"))
    cur=todays_words.items()
    cur.sort(key=lambda e:e[1])
    if cur:
        print "Words of the day:"
        for word,(count,time_added) in cur:
            if count>0:
                print ("%-20s(%d)   (%.2f days)" % (word,count,(time.time()-time_added)/86400)).encode('utf-8')
    else:
        print "No new words today :-("

if __name__=='__main__':
    from sys import argv,exit
    import getopt
    optlist, args = getopt.getopt(argv[1:], '',['popular','today']) 

    #user values                                                            
    for o, a in optlist:
        if o == "--popular":
            show_popular_words()
            sys.exit()
        if o == "--today":
            show_todays_words()
            sys.exit()
    
    show_original_stuff()
