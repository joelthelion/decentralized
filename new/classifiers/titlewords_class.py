import datamodel
from bayesian import Bayesian
filter=Bayesian('titlewords.pck',3)

#See http://en.wikipedia.org/wiki/Naive_Bayes_classifier
def predict(link):
    words=link.title.split(" ")
    return filter.predict(words)

def train(links):
    filter.train([(l.title.split(" "),l.evaluation) for l in links])

def print_self():
    print "A naive Bayesian classifier on title words. Selection of words:"
    print filter
