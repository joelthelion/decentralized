#!/usr/bin/env python

class Classifier:
    def rate(self,symbols):
        """Returns a value between 0 (very good) and 1 (very bad)"""
        assert(False)

class DumbClassifier(Classifier):
    def rate(self,symbols):
        return 0.5

class BayesianClassifier(Classifier):
    """This is an implementation of the Robinson-Fisher spam filtering scheme,
        as described on http://www.linuxjournal.com/article/6467"""
    s=1. #Weight of prior data
    x=.5 #assumed probability of new word first appearing in spam
    def __init__(self,user_id):
        import sql
        bayes_data = sql.request("select symbol,good_count,bad_count\
            from bayes_data where user_id=%s" , user_id)
        self.symb_ratio={}

        for symbol,good,bad in bayes_data: #compute f(w) for each word
            self.symb_ratio[symbol]=(BayesianClassifier.s*BayesianClassifier.x + good) / (BayesianClassifier.s + bad + good)
            #print type(symbol),symbol,self.symb_ratio[symbol]
        
    def rate(self,symbols):
        """Returns a value between 0 (very good) and 1 (very bad)"""
        import operator
        import math
        try: H = self.chi2P(-2. * math.log(reduce(operator.mul,[self.symb_ratio.get(a,BayesianClassifier.x) for a in symbols],1.)),2*len(symbols))
        except OverflowError: print "h overflow";H = 0.0
        try: S = self.chi2P(-2. * math.log(reduce(operator.mul,[1. - self.symb_ratio.get(a,BayesianClassifier.x) for a in symbols],1.)),2*len(symbols))
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
