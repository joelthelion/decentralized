import datamodel

#See http://en.wikipedia.org/wiki/Naive_Bayes_classifier

def predict(link):
    words=link.title.split(" ")
    dic=get_dict()
    good,bad=1.,1.
    for w in words:
        if dic.has_key(w):
            ng,nb = dic[w]
            cond=conditional_prob(ngood,nbad)
            good*=cond
            bad*=1-cond
    return good>=bad

def train(links):
    pass

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
