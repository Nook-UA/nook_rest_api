from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, Identity
from ..db.database import Base

class Park(Base):

    __tablename__ = "park"

    id = Column("id", Integer, Identity(start=1, increment=1), primary_key=True)
    name = Column("name", String)
    picture = Column("picture", LargeBinary)
    location = Column("location", String)
    total_spots = Column("total_spots", Integer)
    owner = Column(Integer, ForeignKey("client.id"))

