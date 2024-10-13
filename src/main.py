from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .endpoints.park import router as park_router
from .endpoints.client import router as client_router

# TODO: Add a description here to appear in the Swagger documentation
description = """
"""

app = FastAPI(
    title="Nook Rest API",
    version="1.0.0",
    description=description,
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

app.include_router(park_router)
app.include_router(client_router)


@app.get("/")
def root():
    return {"message": "I want something good to die for. To make it beautiful to live"}
