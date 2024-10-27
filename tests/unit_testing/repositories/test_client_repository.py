import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError
from psycopg2.errors import UndefinedTable
from src.repositories.client import create_client, get_client_by_id
from src.models.client import Client
from src.schemas.client import ClientCreate
from src.repositories import *

Base = database.Base

SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

def test_create_client(db_session):
    new_client = ClientCreate(
        name="Test Client",
        phone="123456789",
        email="test@example.com",
        picture="test.jpg"
    )

    result = create_client(new_client, db_session)
    assert result.name == new_client.name
    assert result.phone == new_client.phone
    assert result.email == new_client.email
    assert result.picture == new_client.picture

def test_get_client_by_id(db_session):
    test_client = Client(name="Test Client", phone="123456789", email="test@example.com", picture="test.jpg")
    db_session.add(test_client)
    db_session.commit()

    result = get_client_by_id(test_client.id, db_session)
    assert result is not None
    assert result.id == test_client.id
    assert result.name == test_client.name

def test_get_client_by_id_nonexistent(db_session):
    result = get_client_by_id(999, db_session)
    assert result is None

def test_get_client_by_id_table_undefined(db_session, monkeypatch):
    def mock_query(*args, **kwargs):
        raise UndefinedTable

    monkeypatch.setattr(db_session, "query", mock_query)

    result = get_client_by_id(1, db_session)
    assert result == {"error": "Table client not exist"}
