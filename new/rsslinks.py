#!/usr/bin/env python

from sqlalchemy.ext.declarative import declarative_base
Base=declarative_base()
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

class Link(Base):
    """A link is a potentially interesting URL, together with all the relevant metadata
    to help evaluate it"""
    __tablename__ = "links"
    id = Column(Integer,primary_key=True)
    url = Column(String)

