#filter links based on source
import datamodel
from bayesian import Bayesian
filter=Bayesian('sources.pck',5)

#See http://en.wikipedia.org/wiki/Naive_Bayes_classifier
def predict(link):
    words=[s.source for s in link.sources]
    return filter.predict(words)

def train(links):
    filter.train([([s.source for s in l.sources],l.evaluation) for l in links])

def print_self():
    print "A naive Bayesian classifier on link source. Selection of sources:"
    print filter
