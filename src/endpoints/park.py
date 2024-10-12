from fastapi import FastAPI, HTTPException, APIRouter
from ..schemas.park import Park

router = APIRouter(
    tags=["park"],
    prefix="/park"
)


@router.get("/{client_id}")
def get_client_parks(client_id: int) -> int:
    return client_id
