from pydantic import BaseModel
from ..models.client import Client

class ClientBase(BaseModel):
    name: str
    email: str

class ClientCreate(ClientBase):
    id: str

class ClientResponse(ClientBase):
    def from_client(client: Client):
        return ClientResponse(name=client.name, email=client.email)


