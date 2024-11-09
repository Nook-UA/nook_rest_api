from pydantic import BaseModel

class ClientBase(BaseModel):
    name: str
    phone: str
    email: str
    picture: str

class ClientCreate(ClientBase):
    pass

class ClientSchema(ClientBase):
    id: int

    class Config:
        from_attributes = True


