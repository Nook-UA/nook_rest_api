from fastapi import APIRouter, HTTPException
from ..schemas.park import Park
from .client import clients
from http import HTTPStatus


router = APIRouter(tags=["park"], prefix="/park")


parks = [
    Park(
        id=0,
        name="Shopping",
        picture="Leiria.png",
        location="Leiria",
        total_spots=12,
        owner=clients[0],
    ),
    Park(
        id=1,
        name="Garagem",
        picture="Garagem.png",
        location="Leiria",
        total_spots=20,
        owner=clients[1],
    ),
    Park(
        id=2,
        name="Forum",
        picture="Forum.png",
        location="Aveiro",
        total_spots=8,
        owner=clients[1],
    ),
]


@router.get("")
def get_client_parks(client_id: int = None, location: str = None) -> list[Park]:
    """Retrieve Collection of Parks

    Args:
       - client_id (int, optional): Allows to filter Parks by owner_id. Defaults to Any.
       - location (str, optional): Allows to filter by location. Defaults to Any.

    Returns:
       - list[Park]: List of all the Parks matching the filter conditions.
    """
    response = parks
    if client_id:
        response = [park for park in response if park.owner.id == client_id]
    if location:
        response = [
            park for park in response if park.location.lower() == location.lower()
        ]
    return response


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
    try:
        return parks[park_id]
    except IndexError:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail=f"Park with {park_id=} does not exist.")