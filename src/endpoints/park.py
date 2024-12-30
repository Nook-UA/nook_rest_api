from fastapi import APIRouter, HTTPException, Depends
from http import HTTPStatus
from sqlalchemy.orm import Session

import requests
from ..settings import settingObj

from ..schemas.park import Park, ParkCreate, ParkResponse, NearbyParkResponse
from ..schemas.parking_spot import ParkingSpotCreate
from ..db.database import get_db
from ..repositories.parks import get_park_by_id, get_parks, get_parks_by_owner_id, create_park
from ..repositories.client import get_client_by_id
from ..repositories.parking_spot import add_parking_spots, set_parking_spots, clear_parking_spots
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
        if distance < max_dist:
            nearby_parks.append(NearbyParkResponse.from_park(park, distance))
    
    return nearby_parks

@router.get("")
def get_parks_endpoint(id_token = Depends(cognito_jwt_authorizer_id_token), session: Session = Depends(get_db)) -> list[ParkResponse]:
    
    client_id = id_token["sub"]
    assert client_exists(client_id, session)

    parks = get_parks_by_owner_id(client_id, session)
    response = [ParkResponse.from_park(park) for park in parks]
    return response

@router.get("/{park_id}")
def get_park_endpoint(park_id: int, id_token = Depends(cognito_jwt_authorizer_id_token), session: Session = Depends(get_db)) -> ParkResponse:
    park = get_park_by_id(park_id, session)
    
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
        response_park = ParkResponse.from_park(created_park)

        # try post to park detection
        body = {
            "id":str(response_park.id),
            "rstp_url":str(response_park.rtsp_url)
        }
        added_park_response = requests.post(settingObj.park_service_url + "/add_parking_lot",json=body)
        if (not added_park_response.ok):
            raise HTTPException(HTTPStatus.BAD_REQUEST, detail=f"Error adding parking lot to the parking detection")

        return response_park
    except Exception as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail=str(e))
    
@router.put("/spots", summary="Add parking spots to a parking lot")
def add_parking_spots_endpoint(park_id: int, spots: list[ParkingSpotCreate], id_token = Depends(cognito_jwt_authorizer_id_token), session: Session = Depends(get_db)) -> ParkResponse:    
    client_id = id_token["sub"]
    assert client_exists(client_id, session)
    
    park = get_park_by_id(park_id, session)
    
    if not park:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail=f"Park with id '{park_id}' does not exist")

    if park.owner_id != client_id:
        raise HTTPException(HTTPStatus.FORBIDDEN, detail=f"Client does not own this park")
    
    if spots == []:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail=f"List of Parking Spots is empty")
    
    try:        
        existing_spots = [{"name":spot.name, "points":spot.get_points()} for spot in park.parking_spots]
        all_spots = [{"name":spot.name, "points":spot.points} for spot in spots] + existing_spots
        response = requests.post(settingObj.park_service_url + f"/parking_lot/{park_id}/spots", json=all_spots)
        if (not response.ok):
            raise HTTPException(HTTPStatus.BAD_REQUEST, detail=f"Error adding spots to the parking detection")
        
        add_parking_spots(park_id, spots, session)
        return ParkResponse.from_park(get_park_by_id(park_id, session))
    except Exception as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail=str(e))
    
@router.post("/spots", summary="Set the parking spots for a parking lot")
def set_parking_spots_endpoint(park_id: int, spots: list[ParkingSpotCreate], id_token = Depends(cognito_jwt_authorizer_id_token), session: Session = Depends(get_db)) -> ParkResponse:    
    client_id = id_token["sub"]
    assert client_exists(client_id, session)
    
    park = get_park_by_id(park_id, session)
    
    if not park:
        raise HTTPException(HTTPStatus.NOT_FOUND, detail=f"Park with id '{park_id}' does not exist")

    if park.owner_id != client_id:
        raise HTTPException(HTTPStatus.FORBIDDEN, detail=f"Client does not own this park")
    
    try:        
        all_spots = [{"name":spot.name, "points":spot.points} for spot in spots]
        added_spots_response = requests.post(settingObj.park_service_url + f"/parking_lot/{park_id}/spots", json=all_spots)
        if (not added_spots_response.ok):
            raise HTTPException(HTTPStatus.BAD_REQUEST, detail=f"Error adding spots to the parking detection")
        
        if spots == []:
            clear_parking_spots(park_id, session)
        else:
            set_parking_spots(park_id, spots, session)
        
        return ParkResponse.from_park(get_park_by_id(park_id, session))
        
    except Exception as e:
        raise HTTPException(HTTPStatus.BAD_REQUEST, detail=str(e))