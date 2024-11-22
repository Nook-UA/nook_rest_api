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
    
    id = Column(String, primary_key=True, index=True)  # Use Cognito's "sub" as primary key
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

    # client = relationship("Client", back_populates="client")
        
    def __repr__(self):
        return f"<Client(id={self.id}, name={self.name}, email={self.email})>"
    