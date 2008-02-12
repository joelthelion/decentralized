
class Classifier:
    def rate(self,symbols):
        """Returns a value between 0 (very good) and 1 (very bad)"""
        assert(False)
    def train(self,symbols,isgood):
        """Train the filter on a certain number of symbols"""
        assert(False)
        

class BayesianClassifier(Classifier):
    def __init__(self,login):
        import sql
        bayes_data = sql.request("select bayes_data.symbol,bayes_data.good_count,bayes_data.bad_count\
            from bayes_data,kolmognus_user where bayes_data.user_id=kolmognus_user.user_id and kolmognus_user.login=%s" , login)
        symb_ratio={}
        self.sum_good,self.sum_bad=0,0
        for symbol,good,bad in bayes_data:
            symb_ratio[symbol]=float(good)/bad
            sum_good+=good
            sum_bad+=bad
        
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
