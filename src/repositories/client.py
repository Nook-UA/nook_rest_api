from sqlalchemy.orm import Session
from fastapi import Depends

from ..models.client import Client
from ..schemas.client import ClientCreate

from psycopg2.errors import UndefinedTable

def get_client_by_id(client_id: str, db: Session) -> Client:
    try:
        return db.query(Client).filter(Client.id == client_id).first()
    except UndefinedTable:
        return {"error": "Table client does not exist"}
    except Exception as e:
        return {"error": str(e)}

def create_client(client: ClientCreate, db: Session) -> Client:

    db_client = Client(
        id = client.id,
        name = client.name,
        email = client.email,
    )

    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    return db_client