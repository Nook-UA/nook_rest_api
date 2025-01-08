from sqlalchemy import Column, Integer, String, Float, ForeignKey, Identity, LargeBinary
from sqlalchemy.orm import relationship
from ..db.database import Base
from ..models.parking_spot import ParkingSpot

class Park(Base):
    __tablename__ = "park"

    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    name = Column(String, nullable=False)
    picture = Column(String, nullable=True)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    rtsp_url = Column(String, nullable=True)
    owner_id = Column(String, ForeignKey("client.id"))

    # Relationship to ParkingSpot
    parking_spots = relationship("ParkingSpot", back_populates="park", cascade="all, delete-orphan")
