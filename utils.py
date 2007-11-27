#Various stuff used elsewhere

class UntrainedFilterException(Exception):
    pass

class Counter(dict):
    def increment(self,key):
        if self.has_key(key):
            self[key]+=1
        else:
            self[key]=1

datadir="data/"

# A list of common words that should not be considered significative, even if they are well represented in the database
common_words = set(['with', 'is', 'and', 'the', 'of', 'to', 'in', \
    'index', 'http', 'html', 'com', 'has', 'le', 'quot',\
    'a', 'un', 'les', 'on', 'by','www','http','com','org'\
    ,'as','net','for','la','et','htm','par','sur']\
    + [repr(n) for n in range(100)])
