from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from psycopg2.errors import UndefinedTable
import json
from ..models.parking_spot import ParkingSpot
from ..schemas.parking_spot import ParkingSpotCreate

error_message = {"error": "Table parking_spot does not exist"}

def add_parking_spots(park_id: int, spots: list[ParkingSpotCreate], db: Session):
    """
    Create multiple parking spot entries for a given park ID.
    """
    try:
        db_spots = []
        for spot in spots:
            db_spot = ParkingSpot(
                name=spot.name,
                park_id=park_id,
                points=json.dumps(spot.points),  # Serialize points as JSON
            )
            db_spots.append(db_spot)

        # Add all the spots to the session
        db.add_all(db_spots)
        db.commit()  # Commit all at once
        db.refresh(db_spots[0])  # Refresh the first spot (or any one of the spots)
        return db_spots
    except UndefinedTable:
        return error_message
    except SQLAlchemyError as e:
        db.rollback()  # Ensure to roll back the session in case of error
        return {"error": str(e)}

def set_parking_spots(park_id: int, spots: list[ParkingSpotCreate], db: Session):
    """
    Replace all parking spots for a given park ID with a new list of parking spots.
    """
    try:
        # First, delete all existing parking spots for the park
        db.query(ParkingSpot).filter(ParkingSpot.park_id == park_id).delete()
        db.commit()  # Commit deletion

        # Now, create the new parking spots
        db_spots = []
        for spot in spots:
            db_spot = ParkingSpot(
                name=spot.name,
                park_id=park_id,
                points=json.dumps(spot.points),  # Serialize points as JSON
            )
            db_spots.append(db_spot)

        # Add all the new spots to the session
        db.add_all(db_spots)
        db.commit()  # Commit all at once
        db.refresh(db_spots[0])  # Refresh the first spot (or any one of the spots)
        return db_spots
    except UndefinedTable:
        return error_message
    except SQLAlchemyError as e:
        db.rollback()  # Ensure to roll back the session in case of error
        return {"error": str(e)}

def clear_parking_spots(park_id: int, db: Session):
    """
    Delete all parking spots for a given park ID.
    """
    try:
        # Delete all parking spots for the specified park_id
        deleted_rows = db.query(ParkingSpot).filter(ParkingSpot.park_id == park_id).delete()
        db.commit()  # Commit the deletion

        if deleted_rows > 0:
            return {"message": f"{deleted_rows} parking spots deleted for park {park_id}"}
        else:
            return {"message": "No parking spots found for this park"}

    except UndefinedTable:
        return error_message
    except SQLAlchemyError as e:
        db.rollback()  # Rollback the session in case of error
        return {"error": str(e)}