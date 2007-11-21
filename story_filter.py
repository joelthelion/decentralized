import utils
import exceptions
from bayes import Bayes
sfilter = Bayes()

def load_filter():
    try:
        sfilter.load()
        random_untrain() #keep wordlist reasonably small and up-to-date (user tastes tend to change over time)
    except exceptions.IOError: 
        raise utils.UntrainedFilterException()

def filter_text(text):
    result = sfilter.guess(text)
    if len(result) == 0:
        return ("spam",0.5)
    else: 
        pool,prob = max(result,key=lambda x: x[1]) #The answer that counts is from the most probable pool
        if pool == "spam":
            return pool,prob
        else:
            return pool,1-prob #we're interested in the probability of spam

def random_untrain():
    """randomly untrains the filter to keep the database size reasonable
    This implementation should be bias-free, ie. should not remove more from a pool than from another"""
    from random import shuffle
    print sfilter.corpus.tokenCount
    if sfilter.corpus.tokenCount > 15000:
        untrain_factor=0.05
        for pool in sfilter.poolNames():
            multi_keys=[]
            for i in sfilter.pools[pool].keys():
                multi_keys.extend([i] * sfilter.pools[pool][i]) #inefficient, but ok since we don't execute this often
            ntokens=int(untrain_factor * len(multi_keys)) + 1
            shuffle(multi_keys)
            untrained_keys=multi_keys[:ntokens]
            print pool
            print untrained_keys
            sfilter._untrain(sfilter.pools[pool],untrained_keys)
        sfilter.dirty = True
        sfilter.commit()
        print "Randomly untrained filter to keep db size reasonable. There are now %d tokens in the database" % sfilter.corpus.tokenCount

def train_filter(text,spamham="",removeDuplicates=True):
    sfilter.train(spamham,text,removeDuplicates=removeDuplicates)
    sfilter.commit()
    print ("Trained filter for %s on text: %s" % (spamham,text)).encode("ascii","replace")


def backup_wordlist():
    sfilter.backup_wordlist()

def get_pool_keys(number=15):
    """Returns most significative keys for each pool."""
    import utils
    significative={}
    key_diffs=[]
    for k in sfilter.corpus.keys():
        if k not in utils.common_words:
            h = sfilter.pools['ham'].get(k,0)
            if sfilter.pools.has_key('spam'):
                s = sfilter.pools['spam'].get(k,0)
            else : s = 0
            total = sfilter.corpus[k]
            key_diffs.append((k,h-s,total))
    key_diffs.sort(key=lambda x:x[1])
    significative['spam'] = [k for k in key_diffs[:number] if k[1] < 0]
    significative['ham'] =  [k for k in key_diffs[-number:] if k[1] > 0]
    return significative

def get_stats():
    message=""
    significative=get_pool_keys()
    for pool,keys in significative.items():
        message += "   " + pool +"\n"
        message += "\n".join(["%-20s %-6d   %-6d" % i for i in keys]) +"\n" + "\n"
    return message
        
def main():
    load_filter()
    texts = [" This is a scientific story about python and open source","This is a blog about design and css with art and photos","Bush and Cheney should be impeached"]
    for i in texts:
        print i,filter_text(i)
    hapaxes=[]
    for k in sfilter.corpus.keys():
        if sfilter.corpus[k] < 3 : continue #ignore keys with low occurence
        guess=sfilter.guess(k)
        if len(guess) > 0:
            pool,prob=max(guess,key=lambda x:x[1])
            if pool == "ham" : prob = 1 - prob
            hapaxes.append( (k,pool,prob,sfilter.corpus[k]))
        else:
            hapaxes.append( (k,'ham',0.5,sfilter.corpus[k]))
    hapaxes.sort(key=lambda x:x[3])
    for k,pool,p,n in hapaxes:
        mytuple=(k,pool,sfilter.pools['ham'].get(k,0),sfilter.pools['spam'].get(k,0),p,n)
        print "%-25s:\t%-5s\t%dh\t%ds\t%.3f\t%d" %mytuple
    print "corpus ", sfilter.corpus.tokenCount
    print "ham ", sfilter.pools['ham'].tokenCount
    print "spam ",sfilter.pools['spam'].tokenCount

if __name__ == '__main__':
    main()
