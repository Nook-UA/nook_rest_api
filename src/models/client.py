from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from .utils import *
from ..repositories import database

class Client(database.Base):
    
    __tablename__ = "client"
    
    id = id_
    name = name 
    phone = phone
    email = email
    picture = Column(String)
    
    # client = relationship("Client", back_populates="client")
        
    def __repr__(self):
        return f"<Client(id={self.id}, name={self.name}, phone={self.phone}, email={self.email}, picture={self.picture})>"
    