# -*- coding: utf-8 -*-
import logging
from uuid import UUID

import click
from rich.console import Console

from .. import database, models

console = Console()
log = logging.getLogger(__name__)

USERS = [
    dict(
        id=UUID("85ed84e6-0617-49dc-b4fa-09c3e7ad9c87"),
        username="fabian",
        email="fabian@die-schuhs.de",
        name="Fabian Schuh",
    )
]
ACCESS_TOKEN = [
    dict(
        token=UUID("00000000-0000-0000-0000-000000000000"),
        user_id=UUID("85ed84e6-0617-49dc-b4fa-09c3e7ad9c87"),
    )
]
TOPICS = [
    dict(id=UUID("49ae6982-0e36-49ef-bf88-c4bc93f84218"), name="template"),
    dict(id=UUID("71e99747-5546-4d18-8f97-f2f2d09ea036"), name="news"),
]
TEAMS = [
    dict(
        id=UUID("fce2f6e4-18f3-47d5-abc0-2e0e483b3b62"),
        user_id=UUID("85ed84e6-0617-49dc-b4fa-09c3e7ad9c87"),
        name="_",
    ),
    dict(
        id=UUID("528f4008-15cb-4415-87c3-2ead7096fcb1"),
        user_id=UUID("85ed84e6-0617-49dc-b4fa-09c3e7ad9c87"),
        name="obsidian",
    ),
    dict(
        id=UUID("161fbd8f-ed53-41a8-8436-c8f3182a9527"),
        user_id=UUID("85ed84e6-0617-49dc-b4fa-09c3e7ad9c87"),
        name="relay.md",
    ),
]


TEAM_TOPICS = [
    # news@obsidian
    dict(
        id=UUID("5a8be7f0-c359-429f-afdd-235ddb8f5c50"),
        team_id=UUID("528f4008-15cb-4415-87c3-2ead7096fcb1"),
        topic_id=UUID("71e99747-5546-4d18-8f97-f2f2d09ea036"),
    ),
    # news@relay.md
    dict(
        id=UUID("5b7244ae-6a78-4fe9-9825-c0b82ca2a310"),
        team_id=UUID("161fbd8f-ed53-41a8-8436-c8f3182a9527"),
        topic_id=UUID("71e99747-5546-4d18-8f97-f2f2d09ea036"),
    ),
    # templates@_
    dict(
        id=UUID("51dcdaee-27e2-40b6-81a6-c56dca36854b"),
        team_id=UUID("fce2f6e4-18f3-47d5-abc0-2e0e483b3b62"),
        topic_id=UUID("49ae6982-0e36-49ef-bf88-c4bc93f84218"),
    ),
]


@click.group()
def setup():
    pass


@setup.command()
def db():
    database.Base.metadata.create_all(database.engine)


@setup.command()
def dev():
    (db,) = database.get_session()
    for user in USERS:
        db.add(models.User(**user))
    db.commit()
    for access_token in ACCESS_TOKEN:
        db.add(models.AccessToken(**access_token))
    db.commit()
    for topic in TOPICS:
        db.add(models.Topic(**topic))
    db.commit()
    for team in TEAMS:
        db.add(models.Team(**team))
    db.commit()
    for team_topic in TEAM_TOPICS:
        db.add(models.TeamTopic(**team_topic))
    db.commit()
