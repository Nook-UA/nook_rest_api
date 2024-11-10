from pydantic import BaseModel
from .client import ClientSchema


class Park(BaseModel):
    id: int
    name: str
    picture: str
    location: str
    total_spots: int
    rtsp_url: str
    owner: int

class ParkCreate(Park):
    pass

# send to detection micrserv
#  rtsp_url -> url do feed de video
#  park_id -> id do parque

# /video_streams
# get -> retorna todos os video streams