
import database as db
from sqlalchemy import Table, Column, Boolean,Float, Integer, Unicode,DateTime,ForeignKey
from sqlalchemy.orm import relation,backref

class Link(db.Base):
    """A link is a potentially interesting URL, together with all the relevant metadata
    to help evaluate it"""
    __tablename__ = "links"
    url = Column(Unicode,primary_key=True)
    title = Column(Unicode)
    sources = relation("LinkSource",backref=backref('link'))
    predictions = relation("Prediction",backref=backref('link'))
    combined_prediction = Column(Boolean)
    date = Column(DateTime)
    """The two next columns are filled when the user evaluated the link"""
    evaluation = Column(Boolean) #True: good
    evaluation_date = Column(DateTime)
    hidden = Column(Boolean)

    def __init__(self,u,t,d):
        self.url=u
        self.title=t
        self.date=d
    def __repr__(self):
        return self.title.encode('utf-8')+\
            " ( "+self.url.encode('utf-8')+" )"

class LinkSource(db.Base):
    """The sources of a link. Can contain additional pieces of info
    only relevant to a certain source, such as points for a reddit link"""
    __tablename__ = "linksources"
    link_url = Column(Unicode,ForeignKey('links.url'),primary_key=True)
    """source is a source identifier, such as the URL of an RSS feed, or
    the jabber id of a friend"""
    source = Column(Unicode,primary_key=True)
    def __init__(self,l,s):
        self.link_url=l
        self.source=s
    def __repr__(self):
        return "link \"" + self.link_url.encode('utf-8')+"\" linked to by "+self.source.encode('utf-8')

class Prediction(db.Base):
    """For each classifier and for each link, the relevant prediction"""
    __tablename__ = "predictions"
    link_url = Column(Unicode,ForeignKey('links.url'),primary_key=True)
    classifier = Column( Unicode, primary_key=True )
    #Good or bad, as predicted by the classifier
    value = Column(Float())
    def __init__(self,url,cl,v):
        self.link_url,self.classifier,self.value = url, cl, v
    def __repr__(self):
        if value:
            return "%s thinks ( %s ) is good" % (self.classifier,self.link_url)
        else:
            return "%s thinks ( %s ) is bad" % (self.classifier,self.link_url)

db.Base.metadata.create_all(db.engine)    #this is needed for debug only,
                                    #otherwise it should be in a setup script
