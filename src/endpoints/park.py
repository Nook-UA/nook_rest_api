from fastapi import APIRouter, HTTPException, Depends
from ..schemas.park import Park, ParkCreate
from ..db.database import get_db
from sqlalchemy.orm import Session
from .client import clients
from ..repositories.parks import get_park_by_id, get_parks, get_park_by_owner_id, create_park
from ..repositories.client import get_client_by_id
from http import HTTPStatus


router = APIRouter(tags=["park"], prefix="/park")

@router.get("")
def get_client_parks(client_id: int = None, db: Session = Depends(get_db)) -> list[Park]:
    """Retrieve Collection of Parks

    Args:
       - client_id (int, optional): Allows to filter Parks by owner_id. Defaults to Any.

    Returns:
       - list[Park]: List of all the Parks matching the filter conditions.
    """

    parks = []
    if client_id is None:
        parks = get_parks(db)
    else:
        parks = get_park_by_owner_id(client_id, db)

  
    return parks

@router.get("/{park_id}")
def get_park(park_id: int, db: Session = Depends(get_db)) -> Park:
    """Retrive Park by park_id

    Args:
       - park_id (int): Indicates the desired Park.

    Raises:
       - HTTPException: If the park_id does not exist.

    Returns:
       - Park: The Park with the given park_id.
    """
    park = None
    try:
        park = get_park_by_id(park_id, db)
        return park
    except IndexError:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail=f"Park with {park_id=} does not exist.")
    
@router.post("")
def create_park_(park: ParkCreate, db: Session = Depends(get_db)) -> Park:
    """Create a new Park

    Args:
       - park (Park): Park to be created.

    Returns:
       - Park: The created Park.

    Raises:
        - BAD_REQUEST: If the Park could not be created.
    """

    # Validate that the owner exists
    owner = get_client_by_id(park.owner, db)
    if not owner:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail=f"Owner with id {park.owner} does not exist.")
        
    
    created_park = None
    try:
        created_park = create_park(park, db)
        return created_park
    except Exception as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail=str(e))


