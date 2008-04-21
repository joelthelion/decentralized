import cPickle
a=cPickle.load(open(".popurls.pck"))
for i in a:
    print type(i)
cPickle.dump(a[3],open(".popurls_alreadyseen.pck","wb"),-1)
