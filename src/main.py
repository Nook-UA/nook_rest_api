from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from .endpoints.park import router as park_router
from .endpoints.client import router as client_router
from .endpoints.test import router as test_router
from .db.create_database import create_tables
from .db.database import SessionLocal
from .endpoints.authentication import router as auth_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_tables()
    yield

# TODO: Add a description here to appear in the Swagger documentation
description = """
"""

app = FastAPI(
    title="Nook Rest API",
    version="1.0.0",
    description=description,
    lifespan=lifespan,
    license_info={"name": "MIT License", "url": "https://opensource.org/licenses/MIT"},
)

# TODO: Add the allowed origins for CORS here
origins = []

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# TODO: Define set ofendpoints here like this:
# app.include_router(<name of the set of endpoints>, tags=["<tag name>"], prefix="/<prefix>")

app.include_router(router=auth_router, prefix="/api")
app.include_router(park_router)
app.include_router(client_router)
""" Demonstration router for testing purposes of jwt token verification"""
app.include_router(test_router)

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    request.state.db = SessionLocal()
    response = await call_next(request)
    request.state.db.close()
    return response

@app.get("/")
def root():
    return {"message": "I want something good to die for. To make it beautiful to live"}
