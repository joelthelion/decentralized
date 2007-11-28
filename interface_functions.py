#module global stuff
import utils
import exceptions
stories_filename = utils.datadir + "stories.db"
time_prefix = utils.datadir + "timestamp_"

#load old stories database
try:
    f=open(utils.datadir + "old_stories.dat")
    import cPickle
    old_stories = cPickle.load(f)
    f.close()
except exceptions.IOError:
    old_stories = set()

def save_old_stories():
    """Saves the set of old stories, to avoid dupes"""
    import cPickle
    f = open(utils.datadir + "old_stories.dat","wb")
    cPickle.dump(old_stories,f,-1)

def add_old(story):
    import md5
    old_stories.add(md5.md5(story.url).digest())
    save_old_stories()

def is_old(url):
    """returns True if url is in the db of old stories"""
    import md5
    if md5.md5(url).digest() in old_stories:
        return True
    else: return False

def save_stories(stories):
    if stories != None:
        import cPickle as pickle
        f=open(stories_filename,"wb")
        pickle.dump(stories,f,-1)
        f.close()

def load_stories():
    import cPickle as pickle
    try:
        f=open(stories_filename,"rb")
        stories = pickle.load(f)
        return stories
    except:
        return {}

def throttled_get_fresh_stories(feeds,update_function):
    import time
    import cPickle as pickle
    stories=load_stories()
    for feed_name,feed_url,min_time in feeds: #Try to get new stories from each feed
        time_filename =time_prefix+feed_name+".dat"
        try:
            timefile=open(time_filename,"rb")  #Open timestamp file to verify if two requests are not too close in time
            oldtime = pickle.load(timefile)
            timefile.close()
        except:
            #We couldn't read timestamp, get fresh stories anyways
            oldtime=0.
        if time.time() - oldtime > min_time * 60:
            update_function("Getting data from %s..." %feed_name)
            readdeliciousfeed(feed_url,stories)
            timefile=open(time_filename,"wb")
            pickle.dump(time.time(),timefile,-1)
            timefile.close()
        else:
            print "Warning : fresh stories for feed %s failed due to throttling limits" %feed_name
    return stories

def readdeliciousfeed(feedurl,storydict={}):
    import feedparser
    import item_description
    f=feedparser.parse(feedurl)
    print feedurl
    print len(f.entries)
    output=[] #optional debug output
    for i in f.entries:
        if not is_old(i.id): #i.id is simply the story URL
            output.append("+")
            if not storydict.has_key(i.id):
                storydict[i.id]=item_description.DeliciousStory(i.id)
            tagchain=""
            if len(i.tags) != 0:
                tagchain=i.tags[0].term.split()
            i.summary=i.get("summary","")
            storydict[i.id].add_user(i.author,i.title,tagchain,i.summary)
            storydict[i.id].update_score()
        else : output.append(".")
    print "".join(output)
    return storydict

def clean_stories(stories):
    import time
    current_time=time.time()
    print "Cleaning story db..."
    for s in stories.values():
        #if the story is older than twelve hours, and wasn't rated by me, remove it
        #We keep stories I rated to avoid dupes
        age = (current_time - s.creation_time) / 3600 #story age in hours
        if age > 24:
            stories.pop(s.url)
            print s.url
    print "Done!"

def backup_stories():
    import shutil
    try:
        shutil.copy(stories_filename,stories_filename+".bak")
    except:
        print "Warning : could not back story database up"
            
def get_authors(stories):
    authors={}
    for i in stories.values():
        for j in i.liked:
            if not authors.has_key(j):
                authors[j]=1
            else:
                authors[j]+=1
    return authors


def refresh_stories(feeds,update_function):
    update_function("Getting fresh stories...")
    stories=throttled_get_fresh_stories(feeds,update_function)
    clean_stories(stories)
    save_stories(stories)
    return stories

def sort_stories(stories,update_function,show_stories=12):
    update_function("Sorting stories by score...")
    slist=[(s.score,s.url) for s in stories.values() if not is_old(s.url)]
    slist.sort(reverse=True)
    while True:
        changed=False
        for s,u in slist[-show_stories:]:
            if not stories[u].gotadditionalinfo: #rerate everything and make sure we get all info for all stories
                update_function("reevaluating %s"%u[:50])
                stories[u].update_score(deep=True)
                changed=True
        if changed:
            slist=[(s.score,s.url) for s in stories.values() if not is_old(s.url)]
            slist.sort(reverse=True)
        else: break #if nothing changes, then we have the best stories and we can exit
    return slist[-show_stories:] 

def reevaluate_all(stories,update_function):
    import sys
    update_function("Reevaluating all stories...")
    clean_stories(stories)
    for s in stories.values():
        if not is_old(s.url):
            s.update_score()
            sys.stdout.write('.')
            sys.stdout.flush()
    save_stories(stories)
    sys.stdout.write('\n')
    return stories

def get_feeds():
    import story_filter
    feeds=[("delicious_current","http://del.icio.us/rss/recent?min=1",1)] #feed_name,feed url,refresh time. This is the delicious recent feed and should be included all the time
    feed_keys=story_filter.get_pool_keys(number=10)['ham']
    for key,dummy,dummy in feed_keys:
        if not key.startswith("liked_by_") and not key.startswith("special_"): #normal, tag feeds
            feeds.append((key+"_feed","http://del.icio.us/rss/tag/" + key,10)) #refresh every ten minutes
        elif key.startswith("liked_by_"): #user feed
            username = key[9:]
            print "Adding %s's feed" % username
            feeds.append((key+"_feed","http://del.icio.us/rss/" + username,10)) #refresh every ten minutes
    return feeds        

def train_filter(story,pool):
    import story_filter
    story.get_additional_info()
    story_filter.train_filter(story.bogorepresentation(),pool)
    add_old(story)

def manual_train_filter_no_func(ham, spam=False):
    """Trains the filter with words given in function parameters"""
    import story_filter
    weight = 6
    story_filter.train_filter((" "+ham+" ")*weight,"ham",removeDuplicates=False)
    if spam:
        story_filter.train_filter((" "+spam+" ")*weight,"spam",removeDuplicates=False)

def manual_train_filter(trainforspam=False,inputfunc=raw_input):
    """Ask the user for a few words for filter initialization"""
    import story_filter
    import types
    weight=6
    while True:
        ham=inputfunc("Enter a few space separated words describing topics you like: ")
        if type(ham) == types.StringType and ham != "" : break
    story_filter.train_filter((" "+ham+" ")*weight,"ham",removeDuplicates=False)
    if trainforspam:
        while True:
            spam=inputfunc("Enter a few space separated words describing topics you DON'T like: ")
            if type(spam) == types.StringType and spam != "" : break
        story_filter.train_filter((" "+spam+" ")*weight,"spam",removeDuplicates=False)

def get_filter_stats():
    import story_filter
    return story_filter.get_stats()

def load_filter():
    import story_filter
    story_filter.load_filter()
    
def backup():
    backup_stories()
    import story_filter
    story_filter.backup_wordlist()

def main():
    #stories = load_stories()
    #stories = readdeliciousfeed("deliciousrecent.rss",stories)
    stories=throttled_get_fresh_stories([("delicious_current","http://del.icio.us/rss/recent?min=1",1)],lambda x:x)
    clean_stories(stories)
    print "Stories with multiple submitters:"
    print [i for i in stories.values() if len(i.liked) > 1]
    print "prolific authors:"
    print [(name,count) for name,count in get_authors(stories).items() if count > 2]

if __name__ == '__main__':
    main()
