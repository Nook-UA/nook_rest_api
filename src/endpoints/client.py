from ..schemas.client import Client
from fastapi import FastAPI, HTTPException, APIRouter

router = APIRouter(tags=["client"], prefix="/client")

clients = [
    Client(id=0, name="Foo", phone="123456789", email="@this", picture="google.com"),
    Client(id=1, name="Bar", phone="987654321", email="@that", picture="bing.com"),
]


@router.get("")
def get_client(client_id: int = None) -> list[Client] | Client:
    if not client_id:
        return clients
    return clients[client_id]
