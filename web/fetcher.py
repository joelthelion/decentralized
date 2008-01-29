#!/usr/bin/env python

#EXTERNAL API
def add_tag_request(tag):
	pass

#INTERNAL FUNCTIONS
import sql
if __name__ == '__main__':
	db=sql.connect()
	print "connected to database"
	#is incoming full??
	#build url list from recent and requested tags
	#fetch urls
