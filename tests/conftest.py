# -*- coding: utf-8 -*-
"""Configuration for pytest"""
import tempfile
from typing import List, Optional
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.config import Settings, SettingsConfigDict

# monekey patching so we load config properly
Settings.model_config = SettingsConfigDict(  # noqa
    env_file="tests/config.env", env_file_encoding="utf-8"
)

# noqa
from backend import database, models, repos  # noqa
from backend.api import app as api_app
from backend.web import app as web_app


@pytest.fixture(scope="session")
def engine():
    # Temporary file for sqlite
    sqlite_db = tempfile.NamedTemporaryFile().name
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


@pytest.fixture(scope="module")
def web_client():
    yield TestClient(web_app)


@pytest.fixture()
def account(dbsession):
    return repos.user.UserRepo(dbsession).create_from_kwargs(
        username="account",
        email="account@example.com",
        name="Example account",
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
    team_repo = repos.TeamRepo(dbsession)
    topic_repo = repos.TopicRepo(dbsession)
    team_topic_repo = repos.TeamTopicRepo(dbsession)
    user_team_repo = repos.UserTeamRepo(dbsession)

    team_repo.create_from_kwargs(
        name="_",
        user_id=account.id,
    )

    team = team_repo.create_from_kwargs(
        name="myteam",
        user_id=account.id,
        public_permissions=0,
    )
    topic = topic_repo.create_from_kwargs(name="mytopic")
    team_topic_repo.create_from_kwargs(team_id=team.id, topic_id=topic.id)
    # Join account into default team
    user_team_repo.create_from_kwargs(team_id=team.id, user_id=account.id)


@pytest.fixture()
def document_repo(dbsession):
    return repos.DocumentRepo(dbsession)


@pytest.fixture()
def user_repo(dbsession):
    return repos.UserRepo(dbsession)


@pytest.fixture()
def team_repo(dbsession):
    return repos.TeamRepo(dbsession)


@pytest.fixture()
def team_topic_repo(dbsession):
    return repos.TeamTopicRepo(dbsession)


@pytest.fixture
def user_team_topic_repo(dbsession):
    return repos.UserTeamTopicRepo(dbsession)


@pytest.fixture
def user_team_repo(dbsession):
    return repos.UserTeamRepo(dbsession)


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
            tts.append(team_topic_repo.from_string(tt_name, account))
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
        t = team_topic_repo.from_string(team_topic, account)
        return user_team_topic_repo.create_from_kwargs(
            team_topic_id=t.id,
            user_id=acc.id,
        )

    yield func


@pytest.fixture
def create_team(team_repo, account):
    def func(name: str, **kwargs):
        if "user_id" not in kwargs:
            kwargs["user_id"] = account.id
        return team_repo.create_from_kwargs(name=name, **kwargs)

    return func


@pytest.fixture
def create_team_topic(team_topic_repo, account):
    def func(name: str, from_account=account):
        return team_topic_repo.from_string(name, from_account)

    return func


@pytest.fixture
def join_team(user_team_repo):
    def func(team: models.Team, user: models.User, **kwargs):
        return user_team_repo.create_from_kwargs(
            team_id=team.id, user_id=user.id, **kwargs
        )

    return func


@pytest.fixture
def upload_document(api_client):
    def func(content: str, headers: dict, relay_to: Optional[str] = None):
        if not relay_to:
            payload = f"""---
relay-filename: example.md
relay-to: []
---

{content}"""
        else:
            payload = f"""---
relay-filename: example.md
relay-to:
- {relay_to}
---

{content}"""
        req = api_client.post("/v1/doc", headers=headers, content=payload)
        req.raise_for_status()
        res = req.json()
        if "error" in res:
            raise ValueError(res["error"]["code"], res["error"]["message"])
        return res["result"]

    return func


@pytest.fixture
def update_document(api_client):
    def func(id: str, content: str, headers: dict, relay_to: str):
        payload = f"""---
relay-filename: example.md
relay-to:
- {relay_to}
---

{content}"""
        req = api_client.put(f"/v1/doc/{id}", headers=headers, content=payload)
        req.raise_for_status()
        res = req.json()
        if "error" in res:
            raise ValueError(res["error"]["code"], res["error"]["message"])
        return res["result"]

    return func


@pytest.fixture
def patch_document_body_create():
    with patch("backend.repos.document_body.DocumentBodyRepo.create") as mock:
        yield mock


@pytest.fixture
def patch_document_body_get():
    def func(text):
        print("foobar")
        with patch(
            "backend.repos.document_body.DocumentBodyRepo.get_by_id",
            return_value=text.encode("utf-8"),
        ):
            yield

    return func


@pytest.fixture
def patch_document_body_update():
    with patch(
        "backend.repos.document_body.DocumentBodyRepo.update",
    ) as mock:
        yield mock
