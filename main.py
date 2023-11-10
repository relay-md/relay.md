# -*- coding: utf-8 -*-
import logging

import click
import uvicorn

from api import database, models

assert models

log = logging.getLogger(__name__)


@click.group()
def main():
    pass


@main.command()
def db():
    database.Base.metadata.create_all(database.engine)


@main.command()
@click.option("--port", default=5000)
@click.option("--host", default="127.0.0.1")
@click.option("--debug/--no-debug", default=False)
def api(port, host, debug):
    """Run the public API"""
    from api.api import app

    kwargs = dict(port=int(port), host=host)
    if debug:
        kwargs["reload"] = True
        uvicorn.run("api.api:app", **kwargs)
    else:
        uvicorn.run(app, **kwargs)


if __name__ == "__main__":
    main()
