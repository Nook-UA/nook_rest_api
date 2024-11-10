from fastapi import APIRouter, HTTPException
from ..schemas.park import Park, ParkCreate
from .client import clients
from ..repositories.parks import get_park_by_id, get_parks, get_park_by_owner_id, create_park
from http import HTTPStatus


router = APIRouter(tags=["park"], prefix="/park")

@router.get("")
def get_client_parks(client_id: int = None) -> list[Park]:
    """Retrieve Collection of Parks

    Args:
       - client_id (int, optional): Allows to filter Parks by owner_id. Defaults to Any.

    Returns:
       - list[Park]: List of all the Parks matching the filter conditions.
    """

    parks = []
    if client_id is None:
        parks = get_parks()
    else:
        parks = get_parks_by_owner_id(client_id)

  
    return parks

@router.get("/{park_id}")
def get_park(park_id: int) -> Park:
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
        park = get_park_by_id(park_id)
        return park
    except IndexError:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail=f"Park with {park_id=} does not exist.")
    
@router.post("")
def create_park_(park: ParkCreate) -> Park:
    """Create a new Park

    Args:
       - park (Park): Park to be created.

    Returns:
       - Park: The created Park.

    Raises:
        - BAD_REQUEST: If the Park could not be created.
    """
    
    created_park = None
    try:
        created_park = create_park(park)
        return created_park
    except Exception as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail=str(e))


