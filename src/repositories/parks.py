from sqlalchemy.orm import Session
from fastapi import Depends

from ..models.park import Park
from ..schemas.park import ParkCreate

from ..db.database import get_db

from psycopg2.errors import UndefinedTable

#------------------------------------------------
error_message = {"error": "Table park not exist"}
#------------------------------------------------


def create_park(park: ParkCreate, db: Session = Depends(get_db)):
    try:
        db_park = Park(
            name=park.name,
            picture=park.picture,
            location=park.location,
            total_spots=park.total_spots,
            rtsp_url=park.rtsp_url,
            owner=park.owner
        )
        db.add(db_park)
        db.commit()
        db.refresh(db_park)
        return db_park
    except UndefinedTable:
        return error_message
    except Exception as e:
        return {"error": str(e)}


def get_park_by_id(park_id: int, db: Session = Depends(get_db)):
    try:
        return db.query(Park).filter(Park.id == park_id).first()
    except UndefinedTable:
        return error_message
    except Exception as e:
        return {"error": str(e)}
    
def get_park_by_owner_id(owner_id: int, db: Session = Depends(get_db)):
    try:
        return db.query(Park).filter(Park.owner == owner_id).all()
    except UndefinedTable:
        return error_message
    except Exception as e:
        return {"error": str(e)}

def get_parks(db: Session = Depends(get_db)):
    try:
        return db.query(Park).all()
    except UndefinedTable:
        return error_message
    except Exception as e:
        return {"error": str(e)}