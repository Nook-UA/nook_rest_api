import fastapi
from pydantic import BaseModel
import uuid

class Account(BaseModel):
    username: str
    password: str
    token: str

router = fastapi.APIRouter(prefix="/auth", tags=["authentication"])
accounts = {}

@router.post("/signup")
async def signup(username: str, password: str) -> Account:


    if username in accounts.keys():
        raise await fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Username already in use",
        )

    new_account = Account(username=username, password=password, token=str(uuid.uuid4()))
    accounts[username] = new_account

    return new_account


@router.post("/login")
async def login(username: str, password: str) -> Account:

    if username not in accounts.keys():
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Username does not exist",
        )

    account = accounts[username]

    if account.password != password:
        raise fastapi.HTTPException(
            status_code=fastapi.status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password",
        )

    return account