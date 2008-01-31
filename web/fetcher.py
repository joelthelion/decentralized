#!/usr/bin/env python

import sql
import time

def is_incomming_full():
    return sql.request("select count(url) from incoming_url;")[0][0] > 100

def get_url_symbols(url):
    import delicious
    authors,tags,descriptions,date = delicious.get_delicious_data_for_url(url)
    symbols = u' '.join(tags)
    symbols += u'liked_by_' + u' liked_by_'.join(authors)
    return symbols

if __name__ == '__main__':
    import delicious
    import time
    sql.service_set_status('fetcher','started')
    while True:
        #is incoming full??
        #build url list from recent and requested tags
        #fetch urls
        if not is_incomming_full(): #If there are less than 100 urls in the incoming table
            print "Fetch start"
            for url in delicious.get_recent_urls():
                print "Getting symbols"
                symbols = get_url_symbols(url)
                print "Inserting line into incoming"
                query_string = (u"""insert into incoming_url values("%s","%s");""") % (url,symbols)
                sql.query(query_string)
        else:
            print "Incoming full"
            time.sleep(60) 
