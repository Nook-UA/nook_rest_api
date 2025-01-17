
from ..models.client import Client
from ..models.park import Park

from .database import engine

def create_tables():
    Client.metadata.create_all(bind=engine)
    Park.metadata.create_all(bind=engine)