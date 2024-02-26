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

from .config import get_config


class Base(DeclarativeBase):
    pass


def get_session() -> Iterator[Session]:
    """A method that returns a session to interact with the sql database"""
    # need for unittest
    if _db is not None:
        yield _db
    else:
        with scoped_session(SessionLocal)() as session:
            yield session


engine_kwargs = {}
engine_options = get_config().SQLALCHEMY_ENGINE_OPTIONS
if engine_options:
    engine_kwargs = {k: v for k, v in engine_options.model_dump().items() if v}

    # Fine tune for sqlite which is used primarily in unittests
    if "sqlite" in get_config().SQLALCHEMY_DATABASE_URI:
        engine_kwargs.update(
            connect_args={
                "check_same_thread": False,
            }
        )
        # These params are incompatible with sqlite
        engine_kwargs.pop("pool_size", None)
        engine_kwargs.pop("max_overflow", None)

engine = create_engine(get_config().SQLALCHEMY_DATABASE_URI, **engine_kwargs)
SessionLocal = sessionmaker(engine)
_db = None
