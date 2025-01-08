from pydantic import BaseModel
from typing import Optional, List
from ..models.park import Park
from ..schemas.parking_spot import ParkingSpotResponse
from ..settings import settingObj


class Park(BaseModel):
    name: str
    picture: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    rtsp_url: Optional[str] = None


class ParkCreate(Park):
    pass


class ParkResponse(Park):
    id: int
    parking_spots: List[ParkingSpotResponse] = []

    @staticmethod
    def from_park(park: Park):
        return ParkResponse(
            id=park.id,
            name=park.name,
            picture=str(settingObj.s3_url) + str(park.picture),
            latitude=park.latitude,
            longitude=park.longitude,
            rtsp_url=park.rtsp_url,
            parking_spots=[ParkingSpotResponse.from_parking_spot(spot) for spot in park.parking_spots]
        )


class NearbyParkResponse(Park):
    distance: float

    @staticmethod
    def from_park(park: Park, distance: float):
        return NearbyParkResponse(
            id=park.id,
            name=park.name,
            picture=str(settingObj.s3_url) + str(park.picture),
            latitude=park.latitude,
            longitude=park.longitude,
            rtsp_url=park.rtsp_url,
            distance=distance,
        )


# send to detection micrserv
#  rtsp_url -> url do feed de video
#  park_id -> id do parque

# /video_streams
# get -> retorna todos os video streams
