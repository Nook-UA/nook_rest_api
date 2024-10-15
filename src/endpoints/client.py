from ..schemas.client import Client
from fastapi import FastAPI, HTTPException, APIRouter
from http import HTTPStatus

router = APIRouter(tags=["client"], prefix="/client")

clients = [
    Client(id=0, name="Foo", phone="123456789", email="@this", picture="google.com"),
    Client(id=1, name="Bar", phone="987654321", email="@that", picture="bing.com"),
]


@router.get("")
def get_client(client_id: int = None) -> list[Client] | Client:
    """Retrieve Collection of Clients or a single Client

    Args:
       - client_id (int, optional): Indicates a specific Client. Defaults to Any.

    Raises:
       - HTTPException: If the Client does not exist.

    Returns:
       - list[Client] | Client: List of all Clients or a single Client.
    """
    if not client_id:
        return clients
    try:
        return clients[client_id]
    except IndexError:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail=f"Client with {client_id=} does not exist.")
