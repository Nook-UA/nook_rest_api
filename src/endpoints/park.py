from fastapi import APIRouter, HTTPException, Depends
from http import HTTPStatus
from sqlalchemy.orm import Session

from ..schemas.park import Park, ParkCreate, ParkResponse, NearbyParkResponse
from ..db.database import get_db
from ..repositories.parks import get_park_by_id, get_parks, get_parks_by_owner_id, create_park
from ..repositories.client import get_client_by_id
from ..auth import cognito_jwt_authorizer_id_token
from ..utils import distance_between_coordinates


router = APIRouter(tags=["park"], prefix="/park")

# if we get a request with a valid token and the user is not in the database
# it means we have screwd up somewhere else
def client_exists(client_id, session):
    client = get_client_by_id(client_id, session)
    return True if client else False

@router.get("/nearby")
def get_nearby_parks_endpoint(lat: float, lon: float, max_dist: float = 1, session: Session = Depends(get_db)) -> list[NearbyParkResponse]:
    parks = get_parks(session)
    
    nearby_parks = []
    
    for park in parks:
        distance = distance_between_coordinates(lat, lon, park.latitude, park.longitude)
        print(park.name, distance, lat, lon, park.latitude, park.longitude)
        if distance < max_dist:
            nearby_parks.append(NearbyParkResponse.from_park(park, distance))
    
    return nearby_parks

@router.get("")
def get_parks_endpoint(id_token = Depends(cognito_jwt_authorizer_id_token), session: Session = Depends(get_db)) -> list[ParkResponse]:
    
    client_id = id_token["sub"]
    assert client_exists(client_id, session)

    parks = get_parks_by_owner_id(client_id, session)
    print(parks)
    response = [ParkResponse.from_park(park) for park in parks]
    return response

@router.get("/{park_id}")
def get_park_endpoint(park_id: int, id_token = Depends(cognito_jwt_authorizer_id_token), session: Session = Depends(get_db)) -> ParkResponse:
    park = get_park_by_id(park_id, session)
    print(park)
    if not park:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail=f"Park with id '{park_id}' does not exist")

    if park.owner_id != id_token["sub"]:
        raise HTTPException(HTTPStatus.FORBIDDEN, detail=f"Client does not own this park")

    response = ParkResponse.from_park(park)
    return response

@router.post("")
def create_park_endpoint(park: ParkCreate, id_token = Depends(cognito_jwt_authorizer_id_token), session: Session = Depends(get_db)) -> ParkResponse:    
    client_id = id_token["sub"]
    assert client_exists(client_id, session)
    
    try:
        created_park = create_park(park, client_id, session)
        response = ParkResponse.from_park(created_park)
        return response
    except Exception as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail=str(e))