#!/usr/bin/env python
import cPickle
import buzz
import os
import time
already_seen,distinct_use_days,last_use_day,todays_words=buzz.get_object_from_file(os.path.expanduser("~/.popurls_alreadyseen.pck"))
print len(already_seen)
print todays_words
print distinct_use_days
for k,count in todays_words.items():
    todays_words[k]=count,time.time()
print todays_words
#f=open(os.path.expanduser("~/.popurls_alreadyseen.pck"))
#a=cPickle.load(f)
#f.close()
#print sum(count for now,count in a.values())
#for k in a:
#    if len(k)<2:
#        now,count=a[k]
#        a[k]=now,0
#cPickle.dump(a,open(os.path.expanduser("~/.popurls_alreadyseen.pck"),"wb"),-1)
