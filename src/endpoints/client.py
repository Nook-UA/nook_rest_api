from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..db.database import get_db
from ..schemas.client import ClientCreate, ClientResponse
from ..repositories.client import create_client, get_client_by_id
from ..auth import cognito_jwt_authorizer_id_token

router = APIRouter(prefix="/client", tags=["client"])

@router.get("")
def get_client(id_token = Depends(cognito_jwt_authorizer_id_token), session: Session = Depends(get_db)) -> ClientResponse:
    client = get_client_by_id(id_token["sub"], session)

    if not client:
        new_client = ClientCreate(id=id_token["sub"], name=id_token["cognito:username"], email=id_token["email"])
        client = create_client(new_client, session)

    response = ClientResponse.from_client(client)
    return response