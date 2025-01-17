from fastapi import APIRouter,Depends
from ..auth import cognito_jwt_authorizer_id_token

""" Demonstration router for testing purposes of jwt token verification"""

router = APIRouter(prefix="/test", tags=["test"])


@router.get("")
def test(woof = Depends(cognito_jwt_authorizer_id_token)):
    return woof