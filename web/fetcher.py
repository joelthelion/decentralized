#!/usr/bin/env python

import sql
import delicious
import time

def fetch():
    #is incoming full??
    if sql.request("select count(id) from story where rated_date is null")[0][0]<250:
        #build feed list from recent and requested tags
        print "INFO: building feed list"
        feeds=[feed[0] for feed in sql.request("select url from feed where isnull(fetch_date) or addtime(fetch_date,'01:00:00') < now()")]
        stories=[]
        print "INFO: found %d updatable feeds" % len(feeds)
        for k,feed in enumerate(feeds):
            print "INFO: updating %d/%d feed %s" % (k+1,len(feeds),feed)
            stories.extend(delicious.get_stories_for_feed(feed))
            time.sleep(1)

        #fetch stories for symbols
        print "INFO: building updatable stories list"
        stories=[story[0] for story in sql.request("select url from story where isnull(fetch_date) or addtime(fetch_date,'01:00:00') < now()")]
        print "INFO: found %d updatable stories" % len(stories)
        for k,story in enumerate(stories):
            print "INFO: updating %d/%d story %.50s" % (k+1,len(stories),story)
            delicious.get_symbols_for_story(story)
            time.sleep(3)

    else:
        print "INFO: no more urls needed"
    #clean stories with no symbols
    


if __name__ == '__main__':
    import delicious
    sql.service_set_status('fetcher','started')
    fetch()
    sql.service_set_status('fetcher','stopped')
    sql.db.close()
