from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from sqlalchemy import (
    Column,
    Integer,
    Identity,
    String,
)

from ..db.database import Base

class Client(Base):
    
    __tablename__ = "client"
    
    id = Column("id", Integer, Identity(start=1, increment=1), primary_key=True, index=True)
    name = Column("name", String)
    phone = Column("phone", String)
    email = Column("mail", String)
    picture = Column(String)
    
    # client = relationship("Client", back_populates="client")
        
    def __repr__(self):
        return f"<Client(id={self.id}, name={self.name}, phone={self.phone}, email={self.email}, picture={self.picture})>"
    