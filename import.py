import cPickle
import os
a=cPickle.load(open(os.path.expanduser("~/.popurls_alreadyseen.pck")))
for k in a:
    if len(k)<2:
        now,count=a[k]
        a[k]=now,0
cPickle.dump(a,open("/home/joel/.popurls_alreadyseen.pck","wb"),-1)
