import cPickle
import os
f=open(os.path.expanduser("~/.popurls_alreadyseen.pck"))
a=cPickle.load(f)
f.close()
for k in a:
    if len(k)<2:
        now,count=a[k]
        a[k]=now,0
cPickle.dump(a,open(os.path.expanduser("~/.popurls_alreadyseen.pck"),"wb"),-1)
