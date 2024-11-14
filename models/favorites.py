# favorites.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from db.database import Base 

Base = declarative_base()

class Favorites(Base):
    __tablename__ = 'favorites'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
