# -*- coding: utf-8 -*-
"""Configuration for pytest"""

import tempfile

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend import database, models, repos
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
    # SessionMakerForCelery = scoped_session(
    #    sessionmaker(autocommit=False, autoflush=False, bind=connection)
    # )
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


@pytest.fixture()
def account(dbsession):
    return repos.user.UserRepo(dbsession).create_from_kwargs(
        username="account",
        email="account@example.com",
        name="Example account",
        location="DE-CIX",
        oauth_provider=models.user.OauthProvider.GITHUB,
    )


@pytest.fixture
def access_token(account, dbsession):
    return repos.access_token.AccessTokenRepo(dbsession).create_from_kwargs(
        user_id=account.id
    )


@pytest.fixture
def auth_header(access_token):
    return {"X-API-Key": str(access_token.token)}


@pytest.fixture()
def other_account(dbsession):
    return repos.user.UserRepo(dbsession).create_from_kwargs(
        username="account2",
        email="account2@example.com",
        name="Another Example account",
        location="DE-CIX",
        oauth_provider=models.user.OauthProvider.GITHUB,
    )


@pytest.fixture
def other_access_token(other_account, dbsession):
    return repos.access_token.AccessTokenRepo(dbsession).create_from_kwargs(
        user_id=other_account.id
    )


@pytest.fixture
def other_auth_header(other_access_token):
    return {"X-API-Key": str(other_access_token.token)}


@pytest.fixture(autouse=True)
def default_team_topics(dbsession, account):
    team_repo = repos.team.TeamRepo(dbsession)
    topic_repo = repos.topic.TopicRepo(dbsession)
    team_topic_repo = repos.team_topic.TeamTopicRepo(dbsession)

    team = team_repo.create_from_kwargs(
        name="_", user_id=account.id, allow_create_topics=True, is_private=False
    )

    team = team_repo.create_from_kwargs(
        name="myteam", user_id=account.id, is_private=True
    )
    topic = topic_repo.create_from_kwargs(name="mytopic")
    team_topic_repo.create_from_kwargs(team_id=team.id, topic_id=topic.id)
