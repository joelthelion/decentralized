import datamodel
from bayesian import Bayesian
from utils import tokenize
filter=Bayesian('titlewords.pck',3)

#See http://en.wikipedia.org/wiki/Naive_Bayes_classifier
def predict(link):
    words=tokenize(link.title)
    return filter.predict(words)

def train(links):
    filter.train([(tokenize(l.title),l.evaluation) for l in links])

def print_self():
    print "A naive Bayesian classifier on title words. Selection of words:"
    print filter
