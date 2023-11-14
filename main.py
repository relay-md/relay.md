# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*-

import click

from backend.cli.api import api
from backend.cli.setup import setup
from backend.cli.web import web


@click.group()
def main():
    pass


main.add_command(api)
main.add_command(web)
main.add_command(setup)


if __name__ == "__main__":
    main()
