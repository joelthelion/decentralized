import datamodel

#See http://en.wikipedia.org/wiki/Naive_Bayes_classifier
def predict(link):
    words=link.title.split(" ")
    good,bad=1.,1.
    for w in words:
        if dic.has_key(w):
            ngood,nbad = dic[w]
            cond=conditional_prob(ngood,nbad)
            good*=cond
            bad*=1-cond
    total=good+bad
    good /= total ; bad /= total
    if good>=bad:
        return good
    else:
        return -bad

def train(links):
    dic={}#get_dict()
    for l in links:
        words=l.title.split(" ")
        for w in words:
            good,bad=dic.get(w,(0,0))
            if l.evaluation: good+=1
            else: bad+=1
            dic[w]=(good,bad)
    save_dict(dic)

def get_dict():
    import cPickle
    try:
        return cPickle.load(open(datafile))
    except IOError:
        return {}

datafile='titlewords.pck'
#load the dic only once, on import
dic=get_dict()

def conditional_prob(ngood,nbad):
    uncertainty=1 #this is the central parameter of the classifier. 5 shouldn't be too aggressive
    return float(ngood + uncertainty) / (ngood + nbad + 2*uncertainty)


def save_dict(dic):
    import cPickle
    cPickle.dump(dic,open(datafile,'wb'),-1)

def print_self():
    print "A naive Bayesian classifier on title words. Selection of words:"
    words=dic.items()
    words.sort(key=lambda w:conditional_prob(w[1][0],w[1][1]),reverse=True)
    for ws in words[:5],words[-5:]:
        for w,(g,b) in ws:
            print "%s (%dg,%db,%2.f%%), " %(w.encode('utf-8'),g,b,conditional_prob(g,b)*100.),
        print
