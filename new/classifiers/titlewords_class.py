import datamodel

#See http://en.wikipedia.org/wiki/Naive_Bayes_classifier

def predict(link):
    words=link.title.split(" ")
    dic=get_dict()
    good,bad=1.,1.
    for w in words:
        if dic.has_key(w):
            ngood,nbad = dic[w]
            cond=conditional_prob(ngood,nbad)
            good*=cond
            bad*=1-cond
    return good>=bad

def train(links):
    dic=get_dict()
    for l in links:
        words=l.title.split(" ")
        for w in words:
            good,bad=dic.get(w,(0,0))
            if l.evaluation: good+=1
            else: bad+=1
            dic[w]=(good,bad)
    save_dict(dic)

datafile='titlewords.pck'

def conditional_prob(ngood,nbad):
    uncertainty=5
    return (ngood + uncertainty) / (ngood + nbad + uncertainty)

def get_dict():
    import cPickle
    try:
        return cPickle.load(open(datafile))
    except IOError:
        return {}

def save_dict(dic):
    import cPickle
    cPickle.dump(dic,open(datafile,'wb'),-1)
