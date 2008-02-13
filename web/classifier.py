
class Classifier:
    def rate(self,symbols):
        """Returns a value between 0 (very good) and 1 (very bad)"""
        assert(False)
    def train(self,symbols,isgood):
        """Train the filter on a certain number of symbols"""
        assert(False)

class DumbClassifier(Classifier):
    def rate(self,symbols):
        return 0.5
    def train(self,symbols,isgood): pass

class BayesianClassifier(Classifier):
    """This is an implementation of the Robinson-Fisher spam filtering scheme,
        as described on http://www.linuxjournal.com/article/6467"""
    s=1. #Weight of prior data
    def __init__(self,user_id):
        import sql
        bayes_data = sql.request("select symbol,good_count,bad_count\
            from bayes_data where user_id=%s" , user_id)
        symb_ratio={}
        self.sum_good,self.sum_bad=sql.request("select sum(good_count),sum(bad_count)\
            from bayes_data where user_id=%s",user_id)

        #for symbol,good,bad in bayes_data:
        #    symb_ratio[symbol]=float(good)/(bad+good)
        
    def rate(self,symbols):
        """Returns a value between 0 (very good) and 1 (very bad)"""
        import operator
        product = reduce(operator.mul,[symb_ratio.get(a,1) for a in symbols],1.)
        return 1.  / (1. - product * sum_good/sum_bad)
        
    def train(self,symbols,isgood):
        """Train the filter on a certain number of symbols"""
        assert(False)
    def dump(self):
        import sql
        pass

if __name__ == '__main__':
    b=BayesianClassifier("jojo")
