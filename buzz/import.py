#!/usr/bin/env python
import cPickle
import buzz
import os
import time
#already_seen,distinct_use_days,last_use_day=buzz.get_object_from_file(os.path.expanduser("~/.popurls_alreadyseen.pck"))
already_seen,distinct_use_days,last_use_day,todays_words=buzz.get_object_from_file(os.path.expanduser("~/.popurls_alreadyseen.pck"))
for k,count in todays_words.items():
    todays_words[k]=count,time.time()
print todays_words
cPickle.dump((already_seen,distinct_use_days,last_use_day,todays_words),open(os.path.expanduser("~/.popurls_alreadyseen.pck"),"wb"),-1)
#cPickle.dump((already_seen,distinct_use_days,last_use_day,{}),open(os.path.expanduser("~/.popurls_alreadyseen.pck"),"wb"),-1)
#f=open(os.path.expanduser("~/.popurls_alreadyseen.pck"))
#a=cPickle.load(f)
#f.close()
#print sum(count for now,count in a.values())
#for k in a:
#    if len(k)<2:
#        now,count=a[k]
#        a[k]=now,0
#cPickle.dump(a,open(os.path.expanduser("~/.popurls_alreadyseen.pck"),"wb"),-1)
