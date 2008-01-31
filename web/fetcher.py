#!/usr/bin/env python

import sql
import time

if __name__ == '__main__':
    import delicious
    import time
    sql.service_set_status('fetcher','started',db)
    while True:
        #is incoming full??
        #build url list from recent and requested tags
        #fetch urls
        if sql.request("select count(url) from incoming_url;")[0][0] < 100: #If there are less than 100 urls in the incoming table
            for url in delicious.get_recent_urls():
                sql.query("""insert into incoming_url values("%s","prout");""" % url)
        time.sleep(60) 
