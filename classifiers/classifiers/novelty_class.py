import datamodel
import utils
import cPickle
from bayesian import Bayesian
old_days=30
novel_days=1
hist_bins=8
chronology=utils.open_pickle("novelty.pck",{})
filter=Bayesian('novelty_bayes.pck',5)

def predict(link):
    words=title_words(link.title)
    if not words:
        return 0.
    novelty=sum(1. for w in words if isnovel(w,link.date))/len(words)
    return filter.predict(["novelty_%d"%int(novelty*hist_bins)]) > 0.

def train(links):
    chronology={}
    for l in links:
        words=title_words(l.title)
        for w in words:
            if chronology.has_key(w):
                chronology[w].append(l.date)
            else:
                chronology[w]=[l.date]
    cPickle.dump(chronology,open("novelty.pck","wb",-1))
    training_set=[]
    for l in links:
        words=title_words(l.title)
        novelty=sum(1. for w in words if isnovel(w,l.date))/len(words)
        training_set.append((["novelty_%d"%int(novelty*hist_bins)],l.evaluation))
    filter.train(training_set)

def title_words(title):
    import utils
    return utils.tokenize(title)
    #return [w.lower() for w in title.split()]

def isnovel(word,word_date):
    if not chronology.has_key(word):
        return True
    for date in chronology[word]:
        delta=(word_date-date).days
        if delta > novel_days and delta < old_days:
            return False
    return True

def print_self():
    print "I rate links based on the novelty of the title terms"
    print filter
