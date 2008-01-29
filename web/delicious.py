#!/usr/bin/env python

#delicious content parser for sax xml parser implementation
import xml.sax.handler
class DeliciousHandler(xml.sax.handler.ContentHandler):
	def __init__(self):
		self.in_item=False
		self.in_title=False
		self.in_tag=False
		self.tags={}
	def __repr__(self):
		return '\n'.join([url+': '+title+'\n\t'+' '.join(tags) for url,(title,tags) in handler.tags.items()]).encode('utf-8')

	def startElement(self,name,attributes):
		if name=="item":
			self.current_item=attributes["rdf:about"]
			self.current_title=''
			self.current_tags=''
			self.in_item=True
		elif name=="title":
			self.in_title=True
		elif name=="dc:subject":
			self.in_tag=True
	def characters(self, data):
		if not self.in_item:
			return
		if self.in_title:
			self.current_title+=data
		elif self.in_tag:
			self.current_tags+=data
	def endElement(self,name):
		if name=="dc:subject":
			self.in_tag=False
		elif name=="title":
			self.in_title=False
		elif name=="item":
			self.in_item=False
			self.tags[self.current_item]=(self.current_title,self.current_tags.split(' '))

if __name__=="__main__":
	import sys
	if len(sys.argv)>1:
		feed=sys.argv[1]
	else:
		feed="http://del.icio.us/rss/tag/c++"

	import xml.sax
	handler=DeliciousHandler()
	xml.sax.parse(feed,handler)
	print handler
	print len(handler.tags)
