from pydantic import BaseModel
from typing import List, Tuple
from ..models.park import Park

class ParkingSpot(BaseModel):
    name: str
    points: List[Tuple[float, float]]
    
class ParkingSpotCreate(ParkingSpot):
    pass

class ParkingSpotResponse(ParkingSpot):
    pass
    
    @staticmethod
    def from_parking_spot(spot):
        return ParkingSpotResponse(
            id=spot.id,
            name=spot.name,
            points=spot.get_points()
        )