class Story:
    """This class contains all the information necessary to store data about stories"""
    def __init__(self,url=""):
        import time
        self.url=url #This is the storie's unique identifier
        self.liked=[] #list of *nicks* who liked story
        self.disliked=[] #idem
        self.descriptions={} #per user metadata about the story
        self.score = 0.5 #predicted score : 0 is best, 1 is worst (should be predicted by bogofilter)
        self.creation_time = time.time() #the date (in seconds since epoch) at which the story was first retrieved
        self.update_score()
    def __repr__(self):
        import time
        a="Story: "
        a+= self.url + ", first retrieved on %s " % time.ctime(self.creation_time) + "\n"
        a+= "Liked by : %s\n" % ", ".join(self.liked)
        a+= "Disliked by : %s\n" % ", ".join(self.disliked)
        a+= "Described as:\n"
        for user,text in self.descriptions.iteritems():
            a+="'%s', by %s\n" % (text, user)
        a+="\n"
        return a.encode("utf8")
    def bogorepresentation(self):
        """Returns a representation suitable for a classifier"""
        tokens=[]
        tokens.append(self.url)
        tokens.extend(["liked_by_%s" % user for user in self.liked])
        tokens.extend(["disliked_by_%s" % user for user in self.disliked])
        tokens.extend([description for description in self.descriptions.values()])
        tokens.append("special_always_there") #this is used to measure the overall probability that a story is spam
        return " ".join(tokens).encode("ascii","replace")
    def update_score(self):
        from story_filter import filter_text
        dummy,self.score = filter_text(self.bogorepresentation())


class DeliciousStory(Story):
    def __init__(self,url):
        self.publication_date=None
        self.gotadditionalinfo=False
        self.timedout=False #True if timed out during additional info gathering
        Story.__init__(self,url)
    def add_user(self,nick,title,tags,summary):
        nick=nick.encode("ascii","replace") #take care of users with unicode names
        if not nick in self.liked:
            self.liked.append(nick)
            self.descriptions[nick]=title.encode("ascii","replace")+" "+(" ".join(tags)).encode("ascii","replace")+" "+summary.encode("ascii","replace") #very hackish description, with indifferentiate use of tags and summary. Can be improved in the future
    def get_additional_info(self):
        if not self.gotadditionalinfo:
            self.gotadditionalinfo = True
            import md5
            page_url="http://del.icio.us/rss/url/" + md5.md5(self.url).hexdigest()
            print "Fetched additional info for %s..." % self.url
            from feedparser import parse
            import timeout
            import time
            timed_out=timeout.threadmethod(2)
            try:
                feed=timed_out(parse)(page_url) #timeout and raise exception if the parsing takes too long (more than 2 seconds)
                users=[i.author for i in feed['entries']]
                try:
                    self.publication_date=min([time.mktime(i.updated_parsed) for i in feed['entries']])
                except ValueError : pass #if no dates are found, do nothing
                summaries=[i.summary if i.has_key("summary") else "" for i in feed['entries']]
                tags=[i.tags[0].term.split() for i in feed['entries'] if len(i.tags) != 0]
                for u,s,t in zip(users,summaries,tags):
                    self.add_user(u,"",t,s) # all users usually use the same title, no need to repeat it
                time.sleep(1) # throttling by respect for delicious servers
            except timeout.ThreadMethodTimeoutError:
                print "  Fetching additional info timed out."
                self.timedout=True
    def update_score(self,deep=False):
        from story_filter import filter_text
        if deep: # get more info if requested
            self.get_additional_info()
            dummy,self.score = filter_text(self.bogorepresentation())
        else:
            dummy,self.score = filter_text(self.bogorepresentation())
        #print "Updated score for %s, got %f" % (self.url,self.score)
    def bogorepresentation(self):
        special_tags=""
        if len(self.liked) < 3 and self.gotadditionalinfo and not self.timedout: special_tags += " special_unpopular" #add special tags for stories that are not rated by a lot of people
        if self.timedout: special_tags += " special_timedout "
        if self.publication_date is not None:
            story_age = self.creation_time - self.publication_date
            if story_age < 260000 : special_tags += " special_newsstory " # if story has less than three days, it is news
            elif story_age < 3e7 : special_tags += " special_notold "
            else : special_tags += " special_oldstory " # if story was created more than a year ago, it is old
        return Story.bogorepresentation(self) + special_tags


if __name__ == "__main__":
    #UNIT TESTING
    testitem = Story("http://www.ochef.com/r11.htm")
    testitem.liked=["john","paul"]
    testitem.descriptions={"paul" : "Great Site!"}
    testitem.disliked=["liar66"]
    print testitem

    delstory = DeliciousStory("http://nitle.org/")
    delstory.add_user("joel","my title",["stupid","idiot","useless"],"this is a bogus story")
    print delstory
    print delstory.bogorepresentation()
    delstory.get_additional_info()
    print delstory
    print delstory.bogorepresentation()


