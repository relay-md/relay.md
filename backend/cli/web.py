# -*- coding: utf-8 -*-
import logging

import click
import uvicorn
from rich.console import Console

console = Console()
log = logging.getLogger(__name__)


@click.group()
def web():
    pass


@web.command()
@click.option("--port", default=5000)
@click.option("--host", default="127.0.0.1")
@click.option("--debug/--no-debug", default=False)
def run(port, host, debug):
    """Run the public API"""
    from backend.web import app

    kwargs = dict(port=int(port), host=host)
    if debug:
        kwargs["reload"] = True
        uvicorn.run("backend.web:app", **kwargs)
    else:
        uvicorn.run(app, **kwargs)
