from fastapi import status
from fastapi.testclient import TestClient
from unittest.mock import patch
from src.main import app


BASE_URL = "http://localhost:8000/client"

CLIENT = TestClient(app)



def test_create_client_endpoint():
    test_payload = {
        "name": "client",
        "phone": "987654321",
        "email": "valar@morghulis.got",
        "picture": "string"
    }
    mock_data = test_payload
    mock_data["id"] = 1
    
    with patch("src.endpoints.client.create_client", return_value=mock_data):

        response = CLIENT.post(BASE_URL, json=test_payload)

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == mock_data

def test_get_client_endpoint():
    mock_data = {
        "id": 1,
        "name": "client",
        "phone": "987654321",
        "email": "valar@morghulis.got",
        "picture": "string"
    }
    
    with patch("src.endpoints.client.get_client_by_id", return_value=mock_data):

        response = CLIENT.get(BASE_URL, params={"client_id": 1})

        assert response.status_code == status.HTTP_200_OK
        assert response.json() == mock_data