from pydantic import BaseModel


class Client(BaseModel):
    id: int
    name: str
    phone: str
    email: str
    picture: str

    class Config:
        from_attributes = True
