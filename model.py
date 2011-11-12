from sqlalchemy import *
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
class PokemonType(Base):
    """
    """
    __tablename__ = 'pokemon_type'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)

    def __init__(self, _id, name, description):
        """
        """
        self.id = _id
        self.name = name
        self.description = description
        
class Type(Base):
    """
    """
    __tablename__ = 'type'

    id = Column(Integer, primary_key=True)
    name = Column(String)


    def __init__(self, name):
        """
        
        Arguments:
        - `self`:
        - `name`:
        """
        self.name = name


