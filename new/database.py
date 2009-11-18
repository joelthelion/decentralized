#This module does all the necessary work to initialize sqlalchemy
#To get a connection to the database, just create a Session object

#To handle connections with the database
from sqlalchemy.orm import sessionmaker
Session=sessionmaker()

#Base class for all sql mapped classes
from sqlalchemy.ext.declarative import declarative_base
Base=declarative_base()

#Specify which database we're going to use
from sqlalchemy import create_engine,or_,and_,not_
engine=create_engine("sqlite:///test.db")
Session.configure(bind=engine)

