# -*- coding: utf-8 -*-

import click
from rich.console import Console

from .. import models, repos

console = Console()
MODEL = models.Document


@click.group()
def document_body():
    pass


@document_body.command()
def move_nested():
    """Move into nested subdir structure"""

    repo = repos.DocumentBodyRepo()
    for file in repo.list():
        if file.is_dir:
            continue
        try:
            repo.stat(repo.get_file_name(file.object_name))
            # file exists, continue
            continue
        except Exception:
            console.print(f"copying {file.object_name=}")
            repo.copy(file.object_name, repo.get_file_name(file.object_name))
