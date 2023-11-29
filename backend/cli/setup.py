# -*- coding: utf-8 -*-
import logging
from uuid import UUID

import click
from rich.console import Console

from .. import database, models

console = Console()
log = logging.getLogger(__name__)


@click.group()
def setup():
    pass


@setup.command()
def db():
    database.Base.metadata.create_all(database.engine)


@setup.command()
def dev():
    (db,) = database.get_session()
    user = models.User(
        username="fabian", email="fabian@die-schuhs.de", name="Fabian Schuh"
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    db.add(
        models.AccessToken(
            user_id=user.id, token=UUID("00000000-0000-0000-0000-000000000000")
        )
    )
    topic = models.Topic(name="templates")
    team = models.Team(name="_")
    db.add(team)
    db.add(topic)
    db.commit()
    db.refresh(team)
    db.refresh(topic)
    db.add(models.TeamTopic(team_id=team.id, topic_id=topic.id))
    db.commit()
