from sqlalchemy.orm import Session

from ..models.park import Park
from ..schemas.park import ParkCreate

from psycopg2.errors import UndefinedTable

#------------------------------------------------
error_message = {"error": "Table park not exist"}
#------------------------------------------------


def create_park(park: ParkCreate, owner_id: str, db: Session):
    try:
        db_park = Park(
            name=park.name,
            picture=park.picture,
            latitude=park.latitude,
            longitude=park.longitude,
            rtsp_url=park.rtsp_url,
            owner_id=owner_id
        )
        db.add(db_park)
        db.commit()
        db.refresh(db_park)
        return db_park
    except UndefinedTable:
        return error_message
    except Exception as e:
        return {"error": str(e)}


def get_park_by_id(park_id: int, db: Session):
    try:
        return db.query(Park).filter(Park.id == park_id).first()
    except UndefinedTable:
        return error_message
    except Exception as e:
        return {"error": str(e)}
    
def get_parks_by_owner_id(owner_id: int, db: Session):
    try:
        return db.query(Park).filter(Park.owner_id == owner_id).all()
    except UndefinedTable:
        return error_message
    except Exception as e:
        return {"error": str(e)}

def get_parks(db: Session):
    try:
        return db.query(Park).all()
    except UndefinedTable:
        return error_message
    except Exception as e:
        return {"error": str(e)}