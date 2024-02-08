# -*- coding: utf-8 -*-
from uuid import UUID

import click
from rich.console import Console

from .. import models
from ..database import get_session
from .utils import dump_model, edit_item, new_item, show_item

console = Console()
MODEL = models.Subscription


@click.group()
def subscription():
    pass


@subscription.command()
def list():
    db = next(get_session())
    dump_model(
        db,
        MODEL,
    )


@subscription.command()
def create():
    db = next(get_session())
    new_item(
        db,
        MODEL,
    )


@subscription.command()
@click.argument("id", type=UUID)
def delete(id):
    db = next(get_session())
    item = db.get(MODEL, id)
    if item:
        db.delete(item)
        db.commit()


@subscription.command()
@click.argument("id", type=UUID)
def edit(id):
    db = next(get_session())
    edit_item(db, MODEL, id)


@subscription.command()
@click.argument("id", type=UUID)
def show(id):
    db = next(get_session())
    show_item(db, MODEL, id)
