#!/usr/bin/env python

import sql
import time

def has_enough_urls():
    return sql.request("select count(id) from story where rated_date is null")[0][0] > 50


if __name__ == '__main__':
    import delicious
    import time
    sql.service_set_status('fetcher','started')
    while True:
        #is incoming full??
        if not has_enough_urls(): 
            #build url list from recent and requested tags
	    #fetch stories for symbols
            print "INFO: Fetching symbols start"
            for url in delicious.get_recent_stories():
		#fetch urls
                delicious.get_symbols_for_story(url)
        else:
            print "INFO: fetcher waiting for more urls to be needed"
	#clean stories with no symbols

        print "INFO: sleeping"
        time.sleep(120) 
