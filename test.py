#!/usr/bin/env python
import cPickle
import buzz
import os
import time
already_seen,distinct_use_days,last_use_day,todays_words=buzz.get_object_from_file(os.path.expanduser("~/.popurls_alreadyseen.pck"))
print len(already_seen)
#print todays_words
print distinct_use_days
a=already_seen.items()
a.sort(key=lambda e:distinct_use_days-e[1][0],reverse=True)
print a[:10]
#for k,count in todays_words.items():
#    todays_words[k]=count,time.time()
#print todays_words
#for w,(c,add) in todays_words.items():
#    if c==0:
#        print w.encode("utf-8"),c,time.time()-add
#        todays_words[w]=(c+1,add)
#cPickle.dump((already_seen,distinct_use_days,last_use_day,todays_words),open(os.path.expanduser("~/.popurls_alreadyseen.pck"),"wb"),-1)

#f=open(os.path.expanduser("~/.popurls_alreadyseen.pck"))
#a=cPickle.load(f)
#f.close()
#print sum(count for now,count in a.values())
#for k in a:
#    if len(k)<2:
#        now,count=a[k]
#        a[k]=now,0
#cPickle.dump(a,open(os.path.expanduser("~/.popurls_alreadyseen.pck"),"wb"),-1)
