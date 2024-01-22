# -*- coding: utf-8 -*-
import json
import sys
import uuid

import click
from dateutil.parser import parse
from rich.console import Console
from rich.table import Table
from sqlalchemy import inspect, select

console = Console()


def dump_model(
    db, model, ignore_attributes=[], replace_column_names={}, limit=100, offset=0
):
    table = Table()
    table.add_column("Name")
    attributes = [
        attr for attr in inspect(model).columns.keys() if attr not in ignore_attributes
    ]
    for key in attributes:
        table.add_column(replace_column_names.get(key, key), overflow="fold")
    for item in db.scalars(select(model).limit(limit).offset(offset)):
        table.add_row(
            str(item),
            *[str(getattr(item, key)) for key in attributes],
        )
    console.print(table)


def new_item(
    db, model, ignore_attributes=[], replace_column_names={}, predefined=dict()
):
    ignore_attributes.append("id")
    ignore_attributes = set(ignore_attributes)

    attributes = [
        attr for attr in inspect(model).columns.keys() if attr not in ignore_attributes
    ]
    values = dict()

    for key in attributes:
        value = predefined.get(key)
        if value is None:
            value = click.prompt(replace_column_names.get(key, key), default="")
        if not value:
            continue
        try:
            values[key] = json.loads(value)
        except json.decoder.JSONDecodeError:
            if key.endswith("_id") or key == "token":
                try:
                    values[key] = uuid.UUID(value)
                except Exception:
                    values[key] = value
            elif key.endswith("_time") or key.endswith("_date") or key.endswith("_at"):
                values[key] = parse(value)
            else:
                values[key] = value
    new = model(**values)
    db.add(new)
    db.commit()
    click.echo("✓ Created")
    return new


def edit_item(db, model, id: uuid.UUID, ignore_attributes=[], replace_column_names={}):
    item = db.get(model, id)
    if not item:
        click.echo("Item not found!")
        sys.exit(1)

    ignore_attributes.append("id")
    ignore_attributes = set(ignore_attributes)

    columns = inspect(model).columns
    attributes = [attr for attr in columns.keys() if attr not in ignore_attributes]
    new_values = dict()

    for key in attributes:
        old_value = str(getattr(item, key))
        value = click.prompt(
            replace_column_names.get(key, key), default=old_value or ""
        )
        if not value or value == old_value:
            continue
        try:
            new_values[key] = json.loads(value)
        except json.decoder.JSONDecodeError:
            if key.endswith("_id") or key == "token":
                try:
                    new_values[key] = uuid.UUID(value)
                except Exception:
                    new_values[key] = value
            elif key.endswith("_time") or key.endswith("_date"):
                new_values[key] = parse(value)
            else:
                new_values[key] = value

    for key, value in new_values.items():
        setattr(item, key, value)
    db.commit()
    click.echo("✓ Updated")


def show_item(db, model, id: uuid.UUID, ignore_attributes=[], replace_column_names={}):
    item = db.get(model, id)
    if not item:
        click.echo("Item not found!")
        sys.exit(1)

    table = Table()
    table.add_column("Key")
    table.add_column("Value", overflow="fold")
    attributes = [
        attr for attr in inspect(model).columns.keys() if attr not in ignore_attributes
    ]
    for key in attributes:
        table.add_row(replace_column_names.get(key, key), str(getattr(item, key)))
    console.print(table)
