import datamodel
import cPickle
old_days=30
novel_days=1
try:
    cfile=open("novelty.pck")
    chronology=cPickle.load(cfile)
    cfile.close()
except IOError:
    chronology={}

def predict(link):
    words=title_words(link.title)
    if words: novelty=sum(1. for w in words if isnovel(w,link.date))/len(words)
    else: novelty=0
    return 2*novelty -0.8

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
