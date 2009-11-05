#!/usr/bin/env python

class Classifier:
    def rate(self,symbols):
        """Returns a value between 0 (very good) and 1 (very bad)"""
        assert(False)

class DumbClassifier(Classifier):
    def rate(self,symbols):
        return 0.5

def get_alluser_info():
    import sql
    alluser_info={}
    uncertainty=0.3
    for symbol,good,bad in sql.request("select symbol,sum(good_count),sum(bad_count) from bayes_data group by symbol"):
        alluser_info[symbol]=(float(good) / float(bad + good))*(1-uncertainty)+uncertainty*0.5
    #for k,v in alluser_info.items():
    #    print v,k
    return alluser_info

class BayesianClassifier(Classifier):
    """This is an implementation of the Robinson-Fisher spam filtering scheme,
        as described on http://www.linuxjournal.com/article/6467"""
    s=1. #Weight of prior data
    x=.5 #assumed probability of new word first appearing in spam
    def __init__(self,user_id,alluser_info={}):
        import sql
        self.alluser_info=alluser_info
        bayes_data = sql.request("select symbol,good_count,bad_count\
            from bayes_data where user_id=%s" , user_id)
        self.symb_ratio={}
        liked_symbols=set(sql.request("select liked_symbols from kolmognus_user where id=%s",user_id)[0][0].split())
        for symbol,good,bad in bayes_data: #compute f(w) for each word
            if symbol in liked_symbols:
                good+=5 #empirical bonus added to symbols the user manually tagged as good
            self.symb_ratio[symbol]=(BayesianClassifier.s*self.get_prior_value(symbol) + good) / (BayesianClassifier.s + bad + good)
            #print type(symbol),symbol,self.symb_ratio[symbol]
        
    def get_prior_value(self,symbol):
        return self.alluser_info.get(symbol,BayesianClassifier.x)
    def rate(self,symbols):
        """Returns a value between 0 (very good) and 1 (very bad)"""
        import operator
        import math
        try: H = self.chi2P(-2. * math.log(reduce(operator.mul,[self.symb_ratio.get(a,self.get_prior_value(a)) for a in symbols],1.)),2*len(symbols))
        except OverflowError: print "h overflow";H = 0.0
        try: S = self.chi2P(-2. * math.log(reduce(operator.mul,[1. - self.symb_ratio.get(a,self.get_prior_value(a)) for a in symbols],1.)),2*len(symbols))
        except OverflowError: print "s overflow";S = 0.0
        #print symbols,H,S,(1+H-S)/2.,[i for i in symbols],[self.symb_ratio.get(a,BayesianClassifier.x) for a in symbols]
        #print self.symb_ratio.items()
        return (1+H-S)/2.
        
    def chi2P(self,chi, df):
        """ return P(chisq >= chi, with df degree of freedom)

        df must be even
        """
        import math
        assert df & 1 == 0
        m = chi / 2.0
        mysum = term = math.exp(-m)
        for i in range(1, df/2):
            term *= m/i
            mysum += term
        return min(mysum, 1.0)

if __name__ == '__main__':
    b=BayesianClassifier(2)
