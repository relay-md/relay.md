# -*- coding: utf-8 -*-
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from . import exceptions
from .config import config
from .database import Base, engine
from .routes import v1

# Create all tables
Base.metadata.create_all(engine)

app = FastAPI()
app.include_router(v1.router)

# Set all CORS enabled origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=config.API_ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["Content-Range"],
)

@app.get("/health")
def health():
    return "ok"

exceptions.include_app(app)
