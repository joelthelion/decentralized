#!/usr/bin/env python

import sql
import time

retry_delay=30
def main():
        #start service
	db=sql.connect_db()
        sql.service_set_status('fetcher','started',db)
	print "connected to database"
        while True:
                #is incoming full??
                if sql.is_incoming_full(db):
                        print 'incoming full: sleeping for %d secs' % retry_delay
                        time.sleep(retry_delay)
                        continue

                print "start fetching"
                #build url list from recent and requested tags
                tags=sql.tag_list(db)
                print "available tags: "+' '.join(tags)
                #fetch urls
                aa=raw_input('hello$')
        sql.service_set_status('fetcher','stopped',db)

if __name__ == '__main__':
        try:
                main()
        except EOFError:
                pass
