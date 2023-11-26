# -*- coding: utf-8 -*-
"""Configuration for pytest"""

import tempfile
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from backend import config, database, models
from backend.api import app as api_app


# Temporary file for sqlite
sqlite_db = (
    tempfile.NamedTemporaryFile().name
)  # CHANGES - Do we need the immediete deletion behavior or should we change the file name to "tempfile.mkstemp()"?


@pytest.fixture(scope="session")
def engine():
    database.engine = create_engine(
        f"sqlite:///{sqlite_db}",
        echo=False,
        connect_args={"check_same_thread": False},
    )
    return database.engine


@pytest.fixture(scope="session")
def tables(engine):
    database.Base.metadata.create_all(engine)
    yield
    database.Base.metadata.drop_all(engine)


@pytest.fixture(scope="function")
def dbsession(engine, tables):
    """Returns an sqlalchemy session, and after the test tears down everything
    properly."""
    # https://stackoverflow.com/a/60978927
    connection = engine.connect()
    # begin the nested transaction
    transaction = connection.begin()
    # use the connection with the already started transaction
    database.SessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=connection
    )
    session = database.SessionLocal()

    # Update fastapi database
    database._db = session

    # We need a separate session for the async tasks
    SessionMakerForCelery = scoped_session(
        sessionmaker(autocommit=False, autoflush=False, bind=connection)
    )
    # BaseTask._db = SessionMakerForCelery()

    try:
        yield session
    except Exception:
        session.rollback()
    finally:
        session.close()

    # roll back the broader transaction
    transaction.rollback()
    # put back the connection to the connection pool
    connection.close()


@pytest.fixture(scope="module")
def api_client():
    yield TestClient(api_app)
