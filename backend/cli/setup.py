# -*- coding: utf-8 -*-
import logging

import click
from rich.console import Console

from .. import database

console = Console()
log = logging.getLogger(__name__)


@click.group()
def setup():
    pass


@setup.command()
def db():
    database.Base.metadata.create_all(database.engine)
