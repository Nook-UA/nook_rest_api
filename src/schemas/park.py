from pydantic import BaseModel
from typing import Optional
from ..models.park import Park

class Park(BaseModel):
    name: str
    picture: Optional[bytes] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    rtsp_url: Optional[str] = None

class ParkCreate(Park):
    pass

class ParkResponse(Park):
    id: int

    def from_park(park: Park):
        return ParkResponse(id=park.id, name=park.name, picture=park.picture, latitude=park.latitude, longitude=park.longitude, rtsp_url=park.rtsp_url)


# send to detection micrserv
#  rtsp_url -> url do feed de video
#  park_id -> id do parque

# /video_streams
# get -> retorna todos os video streams