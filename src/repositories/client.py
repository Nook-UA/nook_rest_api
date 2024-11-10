from sqlalchemy.orm import Session
from fastapi import Depends

from ..models.client import Client
from ..schemas.client import ClientCreate
from ..db.database import get_db

from psycopg2.errors import UndefinedTable

def get_client_by_id(client_id: int, db: Session = Depends(get_db)):
    try:
        return db.query(Client).filter(Client.id == client_id).first()
    except UndefinedTable:
        return {"error": "Table client not exist"}
    except Exception as e:
        return {"error": str(e)}

def create_client(client: ClientCreate, db: Session = Depends(get_db)):

    db_client = Client(
        name = client.name,
        phone = client.phone,
        email = client.email,
        picture = client.picture,
    )

    db.add(db_client)
    db.commit()
    db.refresh(db_client)

    return db_client