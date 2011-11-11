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
        
