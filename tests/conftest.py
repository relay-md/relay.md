# -*- coding: utf-8 -*-
"""Configuration for pytest"""

import tempfile
from typing import List

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend import database, models, repos
from backend.api import app as api_app
from backend.repos.document import DocumentRepo
from backend.repos.team import TeamRepo
from backend.repos.team_topic import TeamTopicRepo
from backend.repos.user import UserRepo
from backend.repos.user_team_topic import UserTeamTopicRepo

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


@pytest.fixture()
def eve(dbsession):
    return repos.user.UserRepo(dbsession).create_from_kwargs(
        username="eve",
        email="eve@example.com",
        name="Another Example account",
        location="DE-CIX",
        oauth_provider=models.user.OauthProvider.GITHUB,
    )


@pytest.fixture
def eve_access_token(eve, dbsession):
    return repos.access_token.AccessTokenRepo(dbsession).create_from_kwargs(
        user_id=eve.id
    )


@pytest.fixture
def eve_auth_header(eve_access_token):
    return {"X-API-Key": str(eve_access_token.token)}


@pytest.fixture(autouse=True)
def default_team_topics(dbsession, account):
    team_repo = repos.team.TeamRepo(dbsession)
    topic_repo = repos.topic.TopicRepo(dbsession)
    team_topic_repo = repos.team_topic.TeamTopicRepo(dbsession)

    team = team_repo.create_from_kwargs(
        name="_",
        user_id=account.id,
        allow_create_topics=True,
        type=models.team.TeamType.PUBLIC,
    )

    team = team_repo.create_from_kwargs(
        name="myteam", user_id=account.id, type=models.team.TeamType.PRIVATE
    )
    topic = topic_repo.create_from_kwargs(name="mytopic")
    team_topic_repo.create_from_kwargs(team_id=team.id, topic_id=topic.id)


@pytest.fixture()
def document_repo(dbsession):
    return DocumentRepo(dbsession)


@pytest.fixture()
def user_repo(dbsession):
    return UserRepo(dbsession)


@pytest.fixture()
def team_repo(dbsession):
    return TeamRepo(dbsession)


@pytest.fixture()
def team_topic_repo(dbsession):
    return TeamTopicRepo(dbsession)


@pytest.fixture
def user_team_topic_repo(dbsession):
    return UserTeamTopicRepo(dbsession)


@pytest.fixture
def create_document(account, team_topic_repo, user_repo, document_repo):
    def func(
        filename: str,
        team_topics: List[str] = [],
        users: List[str] = [],
        is_public: bool = False,
    ):
        tts = list()
        for tt_name in team_topics:
            tts.append(team_topic_repo.from_string(tt_name))
        us = list()
        for user in users:
            us.append(user_repo.from_string(user))
        return document_repo.create_from_kwargs(
            filename=filename,
            team_topics=tts,
            user_id=account.id,
            users=us,
            is_public=is_public,
        )

    yield func


@pytest.fixture
def subscribe_to_team_topic(account, team_topic_repo, user_team_topic_repo):
    def func(team_topic: str, acc=account):
        t = team_topic_repo.from_string(team_topic)
        return user_team_topic_repo.create_from_kwargs(
            team_topic_id=t.id,
            user_id=acc.id,
        )

    yield func


@pytest.fixture
def create_team(team_repo, account):
    def func(
        name: str,
        type: models.team.TeamType = models.team.TeamType.PUBLIC,
        allow_create_topics: bool = False,
    ):
        return team_repo.create_from_kwargs(
            name=name,
            user_id=account.id,
            type=type,
            allow_create_topics=allow_create_topics,
        )

    return func


@pytest.fixture
def create_team_topic(team_topic_repo):
    def func(name: str):
        return team_topic_repo.from_string(name)

    return func
