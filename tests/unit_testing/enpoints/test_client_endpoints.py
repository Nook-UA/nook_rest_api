import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from src.main import app
from src.db.database import get_db
from sqlalchemy.orm import Session
from src.models.client import Client
from src.repositories.client import get_client_by_id, create_client
from src.auth import cognito_jwt_authorizer_id_token
from src.schemas.client import ClientCreate, ClientResponse

import pytest
from fastapi.testclient import TestClient
from unittest.mock import MagicMock
from src.main import app
from src.auth import CognitoJWTAuthorizer, cognito_jwt_authorizer_id_token  # Import the actual CognitoJWTAuthorizer

mock_client = Client(
    id="some_user_id",
    name="testuser",
    email="testuser@example.com"
)

mock_claims = {
    "sub": "some_user_id",
    "cognito:username": "testuser",
    "email": "testuser@example.com",
    "token_use": "id",
    "aud": "some_client_id",
}

class MockCognitoJWTAuthorizer:
    def __init__(self, required_token_use, aws_default_region, cognito_user_pool_id, cognito_app_client_id, jwks_client):
        pass

    def __call__(self, authorization: str = None):
        return mock_claims


client = TestClient(app)

@pytest.fixture(scope="module")
def mock_dependencies():
    db = MagicMock(spec=Session)
    app.dependency_overrides[get_db] = lambda: db
    app.dependency_overrides[cognito_jwt_authorizer_id_token] = MockCognitoJWTAuthorizer(
        "id",
        "us-east-1",
        "us-east-1_cognito_pool",
        "some_client_id",
        None
    )
    yield db


def test_create_client(mock_dependencies):
    # Simulate the behavior when the `get_client_by_id` doesn't find the client
    mock_dependencies.query.return_value.filter.return_value.first.side_effect = [None, mock_client]

    response = client.get("/client")
    
    assert response.status_code == 200
    assert response.json() == ClientResponse.from_client(mock_client).model_dump()

def test_get_client(mock_dependencies):
    # Simulate the behavior when the `get_client_by_id` finds the client
    mock_dependencies.query.return_value.filter.return_value.first.side_effect = [mock_client]

    response = client.get("/client")
    
    assert response.status_code == 200
    assert response.json() == ClientResponse.from_client(mock_client).model_dump()