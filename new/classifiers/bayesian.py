class Bayesian:
    def __init__(self,filename):
        self.filename=filename
        import cPickle
        try:
            self.dic = cPickle.load(open(self.filename))
        except IOError:
            self.dic = {}
    def predict(self,words):
        good,bad=1.,1.
        for w in words:
            if self.dic.has_key(w):
                ngood,nbad = self.dic[w]
                cond=self.conditional_prob(ngood,nbad)
                good*=cond
                bad*=1-cond
        total=good+bad
        good /= total ; bad /= total
        if good>=bad:
            return good
        else:
            return -bad
    def train(self,training_set):
        self.dic={}#get_dict()
        for words,evaluation in training_set:
            for w in words:
                good,bad=self.dic.get(w,(0,0))
                if evaluation: good+=1
                else: bad+=1
                self.dic[w]=(good,bad)
        save_dict()
    def save_dict(self,):
        import cPickle
        cPickle.dump(self.dic,open(self.filename,'wb'),-1)
    def conditional_prob(self,ngood,nbad):
        uncertainty=1 #this is the central parameter of the classifier. 5 shouldn't be too aggressive
        return float(ngood + uncertainty) / (ngood + nbad + 2*uncertainty)
    def __repr__(self):
        result=""
        words=self.dic.items()
        words.sort(key=lambda w:self.conditional_prob(w[1][0],w[1][1]),reverse=True)
        for ws in words[:5],words[-5:]:
            for w,(g,b) in ws:
                result+= "%s (%dg,%db,%2.f%%), " %(w.encode('utf-8'),g,b,self.conditional_prob(g,b)*100.)
            result+='\n'
        return result
