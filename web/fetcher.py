#!/usr/bin/env python

import sql
import time

def has_enough_urls():
    return sql.request("select count(id) from story where rated_date is null")[0][0] > 100


if __name__ == '__main__':
    import delicious
    import time
    sql.service_set_status('fetcher','started')
    while True:
        #fetch urls
        #is incoming full??
        if not has_enough_urls(): 
            print "INFO: Fetch start"
            #build url list from recent and requested tags
            for url in delicious.get_recent_stories():
                print "INFO: Getting symbols"
                symbols = delicious.get_symbols_for_story(url)
                print "INFO: ",symbols
        else:
            print "INFO: fetcher waiting for more urls to be needed"
        print "INFO: sleeping"
        time.sleep(60) 
