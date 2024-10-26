from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey
from .utils import *
from ..repositories import database

class Park(database.Base):

    __tablename__ = "park"

    id = id_
    name = name
    picture = Column("picture", LargeBinary)
    location = Column("location", String)
    total_spots = Column("total_spots", Integer)
    owner = Column(Integer, ForeignKey("client.id"))

