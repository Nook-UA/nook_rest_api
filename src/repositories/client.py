from sqlalchemy.orm import Session

from ..models.client import Client
from ..repositories import database

from psycopg2.errors import UndefinedTable

def get_client_by_id(client_id: int, db: Session):
    try:
        db.query(Client).filter(Client.id == client_id).first()
    except UndefinedTable:
        return {"error": "Table client not exist"}
    except Exception as e:
        return {"error": str(e)}

def create_client(client: type(Client), db: Session):
    db.add(client)
    db.commit()
    db.refresh(client)
    return client