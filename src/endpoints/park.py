from fastapi import APIRouter, HTTPException
from ..schemas.park import Park
from .client import clients
from ..repositories.park import insert_park, select_park, update_park, delete_park
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
    response = parks
    if client_id:
        response = [park for park in response if park.owner.id == client_id]
    if location:
        response = [
            park for park in response if park.location.lower() == location.lower()
        ]
    return response


@router.get("/{park_id}")
def get_park(park_id: int = None) -> Park:
    try:
        return parks[park_id]
    except IndexError:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail=f"Park with {park_id=} does not exist.")