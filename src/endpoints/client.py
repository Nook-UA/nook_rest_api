from ..schemas.client import ClientCreate, ClientSchema
from fastapi import APIRouter, Depends
from ..repositories.client import create_client, get_client_by_id
from ..models.client import Client
from sqlalchemy.orm import Session
from psycopg2.errors import UndefinedTable
from sqlalchemy.exc import ProgrammingError

from ..repositories import database 

router = APIRouter(tags=["client"], prefix="/client")

clients = [
    Client(id=0, name="Foo", phone="123456789", email="@this", picture="google.com"),
    Client(id=1, name="Bar", phone="987654321", email="@that", picture="bing.com"),
]

@router.post("")
def create_client2(client: ClientCreate, session: Session= Depends(database.session)) -> ClientSchema:
    """Create a new Client

    Args:
        - client (Client): Client to be created.

    Returns:
        - Client: Created Client.
    """
    try:
        return create_client(client, session)
    except Exception as e:
        return {"error": str(e)}

@router.get("")
def get_client(client_id: int = None, session: Session= Depends(database.session)) -> list[ClientSchema] | ClientSchema:
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
        return get_client_by_id(client_id, session)
    except ProgrammingError:
        return {"error": "BLAH Server Error"}
    except UndefinedTable:
        return {"error": "BLAH does not exist"}
    except Exception as e:
        print("\n"*3)
        print(type(e))
        
        print("\n"*3)
        return {"error": "###"*30 + str(e)}