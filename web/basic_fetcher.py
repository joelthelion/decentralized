#!/usr/bin/env python

import sql
import delicious
import time

def get_stories(feed,added_by):
    import feedparser , md5
    stories=[]
    for e in feedparser.parse(feed).entries:
        link=e["link"]
        story_age=time.time() - time.mktime(e.updated_parsed)
        if story_age < 260000 : date_symbol = " special_newsstory " # if story has less than three days, it is news
        elif story_age < 3e7 : date_symbol = " special_notold "
        else : date_symbol = " special_oldstory " # if story was created more than a year ago, it is old
        symbols=" ".join(["special_author_"+e.get("author","unknown"),e["title"],date_symbol,"special_rssfeed_"+md5.md5(feed).hexdigest(),"special_feedsubmitter_"+added_by])
        stories.append((link,symbols))
    return stories

def fetch():
    #is incoming full??
    if sql.request("select count(id) from story where rated_date is null")[0][0]<250:
        #build feed list from recent and requested tags
        print "INFO: building feed list"
        feeds=sql.request("select url,added_by from feed where isnull(fetch_date) or addtime(fetch_date,'01:00:00') < now()")
        #feeds=["rss.xml"]
        stories=[]
        print "INFO: found %d updatable feeds" % len(feeds)
        for k,(feed,added_by) in enumerate(feeds):
            print"INFO: updating %d/%d feed %s" % (k+1,len(feeds),feed)
            for url,symbols in get_stories(feed,added_by):
                sql.query("insert into story (url,url_md5,hit_count,symbols,symbol_count,fetch_date) values (%s,md5(%s),0,%s,%s,now())\
                  on duplicate key update id=id" , (url,url,symbols,len(symbols.split()))) #nice hack
                sql.query("insert into feed_story (story_id,feed_id)\
                  select story.id,feed.id\
                  from story,feed\
                  where story.url_md5=md5(%s)\
                  and feed.url_md5=md5(%s)\
                  on duplicate key update story_id=story_id" ,(url,feed)) #nice hack II
            sql.query("update feed set fetch_date=now() where url_md5=md5(%s)",feed)

    else:
        print "INFO: no more urls needed"
    #clean stories with no symbols
    
if __name__ == '__main__':
    import delicious
    sql.service_set_status('fetcher','started')
    fetch()
    sql.service_set_status('fetcher','stopped')
    sql.db.close()
