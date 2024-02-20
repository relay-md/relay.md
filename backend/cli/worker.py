# -*- coding: utf-8 -*-

import logging
import sys

import click
from celery.__main__ import main as celery_main
from rich.console import Console

console = Console()
log = logging.getLogger(__name__)


@click.command()
@click.option(
    "--identifier", help="Identifier worker in case multiple operate in parallel"
)
@click.option(
    "--queue",
    type=str,
    help="Selected queue to deal with",
    default=None,
)
@click.option("--concurrency", type=int, help="Number of concurrent workers", default=1)
@click.option(
    "--loglevel", type=str, help="error, debug, warning, info", default="info"
)
def worker(identifier, queue, concurrency, loglevel):
    """Run the celery worker"""
    # dynamically load all of the the tasks of our stack
    queues = {"celery", "general"}
    if not queue:
        queue = ",".join(list(queues))

    log.info(f"Running on queues: {queues}")

    sys.argv = [
        "celery",
        "-A",
        "backend.tasks.celery",
        "worker",
        "--loglevel={}".format(loglevel.upper()),
        # Fair scheduler
        "-Ofair",
        # make use of multiprocessing since libs are not thread-safe
        "--pool=prefork",
        # Concurrency of multiple workers at once
        "--concurrency={}".format(concurrency),
        # Send task-related events that can be captured by monitors like celery
        # events, celerymon, and others.
        "--task-events",
        # Queues to process
        "-Q",
        queue,
    ]

    if identifier:
        sys.argv.extend(["-n", identifier])
    sys.exit(celery_main())
