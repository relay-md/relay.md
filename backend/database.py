# -*- coding: utf-8 -*-
""" Access to the database and tables
"""
from typing import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import (
    DeclarativeBase,
    Session,
    scoped_session,
    sessionmaker,
)

from .config import config


class Base(DeclarativeBase):
    pass


def get_session() -> Iterator[Session]:
    """A method that returns a session to interact with the sql database"""
    # need for unittest
    if _db is not None:
        yield _db
    else:
        db = scoped_session(SessionLocal)
        try:
            yield db  # type: ignore
        finally:
            db.close()


engine_kwargs = {k: v for k, v in config.SQLALCHEMY_ENGINE_OPTIONS.dict().items() if v}
engine = create_engine(config.SQLALCHEMY_DATABASE_URI, **engine_kwargs)
SessionLocal = sessionmaker(engine)
_db = None
