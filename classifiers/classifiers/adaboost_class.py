import datamodel
from utils import tokenize,open_pickle,most_frequent_words,most_frequent_duos,mash_post

class HasWordsPredicate:
    def __init__(self,words):
        self.words=words
    def __call__(self,title):
        return all(w in title for w in self.words)
    def __repr__(self):
        return ",".join(self.words).encode('utf-8')

class PredicateClassifier:
    def __init__(self,predicate):
        self.predicate=predicate
    def train(self,titles,weights,evaluations):
        """titles is [[words]]"""
        total=sum(weights[n]*evaluations[n] for n,words in enumerate(titles) if self.predicate(words))
        self.wordgood=1. if total >= 0 else -1.
    def predict(self,title):
        if self.predicate(title):
            return self.wordgood
        else: return 0.

trained=open_pickle("adaboost.pck",[])

def predict(link):
    #words=tokenize(link.title)
    words=mash_post(link)
    if sum(alpha * c.predict(words) for c,alpha in trained) >= 0:
        return 1.
    else:
        return -1.

def train(links):
    from math import exp,fabs,log
    fwords=most_frequent_words()
    classifiers=[PredicateClassifier(HasWordsPredicate([w])) for w in fwords]
    #classifiers.extend(PredicateClassifier(HasWordsPredicate(duo)) for duo in most_frequent_duos(fwords))
    titles=[mash_post(l) for l in links]
    evaluations=[1. if l.evaluation else -1. for l in links]
    weights=[1./len(links) for l in links]
    trained=[]
    print "Training on %d features..." % len(classifiers)
    while True:
        print ".",
        min_error=1e6 ; best=None
        for c in classifiers:
            c.train(titles,weights,evaluations)
            error=sum(weights[n]*0.5*fabs(c.predict(t)-evaluations[n]) for n,t in enumerate(titles))
            if error < min_error:
                best=c; min_error=error
        if min_error>=0.5:
            print min_error
            break
        Zt=sum(weights[n]*exp(-best.predict(t)*evaluations[n]) for n,t in enumerate(titles))
        weights=[weights[n]*exp(-best.predict(t)*evaluations[n])/Zt for n,t in enumerate(titles)]
        alphat=0.5*log((1-min_error)/min_error)
        trained.append((best,alphat))
        classifiers.remove(best)
    for c,alpha in trained:
        print c.predicate,c.wordgood,alpha
    import cPickle
    cPickle.dump(trained,open("adaboost.pck","wb"),-1)

def print_self():
    print "A simple adaboost classifier on title words with really dumb features"


