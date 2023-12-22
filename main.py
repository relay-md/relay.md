# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import click


@click.group()
def main():
    pass


clis = [
    "backend.cli.api",
    "backend.cli.setup",
    "backend.cli.team",
    "backend.cli.team_topic",
    "backend.cli.topic",
    "backend.cli.user",
    "backend.cli.web",
    "backend.cli.document",
    "backend.cli.document_body",
    "backend.cli.access_token",
    "backend.cli.billing",
    "backend.cli.invoice",
    "backend.cli.subscription",
]

for cli in clis:
    parts = cli.split(".")
    mod = __import__(".".join(parts), fromlist=[parts[-1]])
    main.add_command(getattr(mod, parts[-1]))


if __name__ == "__main__":
    main()
