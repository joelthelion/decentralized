class Bayesian:
    def __init__(self,filename,uncertainty):
        self.uncertainty=uncertainty #this is the central parameter of the classifier. 5 shouldn't be too aggressive
        self.filename=filename
        import cPickle
        try:
            self.dic,self.total_ngood,self.total_links = cPickle.load(open(self.filename))
        except (IOError,ValueError):
            self.dic = {}
    def predict(self,words):
        if self.total_links == 0:
            return 1.0
        good,bad=1.,1.
        for w in words:
            if self.dic.has_key(w):
                ngood,nbad = self.dic[w]
                cond=self.conditional_prob(ngood,nbad)
                good*=cond
                bad*=1-cond
        good*=float(self.total_ngood)/self.total_links
        bad*=float(self.total_links-self.total_ngood)/self.total_links
        total=good+bad
        good /= total ; bad /= total
        if good>=bad:
            return good
        else:
            return -bad
    def train(self,training_set):
        self.dic={}#get_dict()
        self.total_ngood,self.total_links=0,len(training_set)
        for words,evaluation in training_set:
            if evaluation: self.total_ngood+=1
            for w in words:
                good,bad=self.dic.get(w,(0,0))
                if evaluation: 
                    good+=1
                else: bad+=1
                self.dic[w]=(good,bad)
        self.save()
    def save(self):
        import cPickle
        cPickle.dump((self.dic,self.total_ngood,self.total_links),open(self.filename,'wb'),-1)
    def conditional_prob(self,ngood,nbad):
        return float(ngood + self.uncertainty) / (ngood + nbad + 2*self.uncertainty)
    def __repr__(self):
        result=""
        words=self.dic.items()
        words.sort(key=lambda w:self.conditional_prob(w[1][0],w[1][1]),reverse=True)
        for ws in words[:5],words[-5:]:
            for w,(g,b) in ws:
                result+= "%s (%dg,%db,%2.f%%), " %(w.encode('utf-8'),g,b,self.conditional_prob(g,b)*100.)
            result+='\n'
        return result
