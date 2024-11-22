import pytest

from unittest.mock import patch
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from testcontainers.postgres import PostgresContainer

from src.repositories.client import create_client, get_client_by_id
from src.models.client import Client
from src.schemas.client import ClientCreate
from src.db.database import get_db
from src.main import app

postgres_container = PostgresContainer(
    "postgres:15",
    dbname="test_db",
    username="test_user",
    password="test_password"
)


@pytest.fixture(name="session", scope="module")
def setup():
    postgres_container.start()
    connection_url = postgres_container.get_connection_url()
    print(connection_url)
    engine = create_engine(connection_url, connect_args={})
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Client.metadata.create_all(engine)

    def override_get_db():
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    print("Running setup")
    yield SessionLocal
    print("Closing test db")
    postgres_container.stop()


@pytest.fixture(name="test_db", scope="module")
def create_test_db(session):
    db = session()
    print("Creating test db")
    yield db
    print("Closing test db")
    db.close()

@pytest.fixture(name="test_client", scope="function")
def create_user_test(test_db):

    try:
        test_db.query(Client).delete()
        test_db.commit()
    except:
        test_db.rollback()

    test_client = Client(
        id="some_id_1",
        name="Test Client",
        email="test@example.com"
    )

    test_db.add(test_client)
    test_db.commit()
    print("Creating test user")

    yield test_client

    print("Deleting test user")
    test_db.delete(test_client)
    test_db.commit()


def test_create_client(test_db):
    new_client = ClientCreate(
        id="some_id_2",
        name="Test Client",
        email="test@example.com",
    )

    result = create_client(new_client, test_db)
    assert result.id == new_client.id
    assert result.name == new_client.name
    assert result.email == new_client.email

def test_get_client_by_id(test_client, test_db):

    result = get_client_by_id(test_client.id, test_db)

    assert result is not None
    assert result.id == test_client.id
    assert result.name == test_client.name

def test_get_client_by_id_nonexistent(test_db):
    result = get_client_by_id("id_whatever", test_db)
    assert result is None

