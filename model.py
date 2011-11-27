from sqlalchemy import *
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

association_table = Table('association', Base.metadata,
    Column('pokemon_type_id', Integer, ForeignKey('pokemon_type.id')),
    Column('type_id', Integer, ForeignKey('type.id'))
)

class PokemonType(Base):
    """
    """
    __tablename__ = 'pokemon_type'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    types = relationship("Type",
                            secondary=association_table,
                            backref="pokemon_types")


    def __init__(self, _id, name, description):
        """
        """
        self.id = _id
        self.name = name
        self.description = description

    def __repr__(self):
        return "<PokemonType | id: " + repr(self.id) + ", name: "\
            + self.name + ", desc: " + self.description + "types: " + repr(self.types) + ">"

        
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


    def __repr__(self):
        return "<Type | id: " + repr(self.id) + ", name: " + self.name + ">"
