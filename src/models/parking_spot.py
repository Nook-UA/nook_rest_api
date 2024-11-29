from sqlalchemy import Column, Integer, String, ForeignKey, Identity, Text
from sqlalchemy.orm import relationship
from ..db.database import Base
import json


class ParkingSpot(Base):
    __tablename__ = "parking_spot"

    id = Column(Integer, Identity(start=1, increment=1), primary_key=True)
    name = Column(String, nullable=False)
    park_id = Column(Integer, ForeignKey("park.id"), nullable=False)
    points = Column(Text, nullable=False)  # Storing points as JSON string

    # Relationship to Park
    park = relationship("Park", back_populates="parking_spots")

    # Helper methods for points serialization/deserialization
    def set_points(self, points: list[tuple[float, float]]):
        """Store points as a JSON string."""
        self.points = json.dumps(points)

    def get_points(self) -> list[tuple[float, float]]:
        """Retrieve points as a list of tuples."""
        return json.loads(self.points)
