from pydantic import BaseModel
from .client import ClientSchema


class Park(BaseModel):
    id: int
    name: str
    picture: str
    location: str
    total_spots: int
    owner: ClientSchema
