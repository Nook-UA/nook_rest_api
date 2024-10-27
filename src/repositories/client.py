from sqlalchemy.orm import Session

from ..models.client import Client
from ..schemas.client import ClientCreate

from psycopg2.errors import UndefinedTable

def get_client_by_id(client_id: int, db: Session):
    try:
        return db.query(Client).filter(Client.id == client_id).first()
    except UndefinedTable:
        return {"error": "Table client not exist"}
    except Exception as e:
        return {"error": str(e)}

def create_client(client: ClientCreate, db: Session):

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