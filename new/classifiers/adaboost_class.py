import datamodel
from utils import tokenize,open_pickle,most_frequent_words

class HasWordPredicate:
    def __init__(self,word):
        self.word=word
    def __call__(self,words):
        return self.word in words
    def __repr__(self):
        return self.word.encode('utf-8')

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
    words=tokenize(link.title)
    if sum(alpha * c.predict(words) for c,alpha in trained) >= 0:
        return 1.
    else:
        return -1.

def train(links):
    from math import exp,fabs,log
    classifiers=[PredicateClassifier(HasWordPredicate(w)) for w in most_frequent_words()]
    titles=[tokenize(l.title) for l in links]
    evaluations=[1. if l.evaluation else -1. for l in links]
    weights=[1./len(links) for l in links]
    trained=[]
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


