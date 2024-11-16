from pydantic import BaseModel

class ClientBase(BaseModel):
    name: str
    email: str

class ClientCreate(ClientBase):
    id: str

class ClientResponse(ClientBase):
    pass


