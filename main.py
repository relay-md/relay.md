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
    "backend.cli.asset",
    "backend.cli.mautic",
    "backend.cli.stripe_",
]

for cli in clis:
    parts = cli.split(".")
    mod = __import__(".".join(parts), fromlist=[parts[-1]])
    module = parts[-1]
    if parts[-1].endswith("_"):
        module = parts[-1].replace("_", "")
    main.add_command(getattr(mod, module))


if __name__ == "__main__":
    main()
