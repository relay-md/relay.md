# -*- coding: utf-8 -*-


import click
from rich.console import Console

from ..database import get_session
from ..repos.billing import PersonalInformationRepo, SubscriptionRepo
from ..repos.mautic import MauticRepo
from ..repos.user import UserRepo

console = Console()


@click.group()
def mautic():
    pass


@mautic.command()
def from_user():
    (db,) = get_session()
    user_repo = UserRepo(db)
    mautic_repo = MauticRepo()
    for user in user_repo.list():
        mautic_repo.process_user(user)
        click.echo(f"Imported {user.id} / {user.username}")


@mautic.command()
def from_person():
    (db,) = get_session()
    person_repo = PersonalInformationRepo(db)
    mautic_repo = MauticRepo()
    for person in person_repo.list():
        mautic_repo.process_person(person)
        click.echo(f"Imported {person.id} / {person.user.username}")


@mautic.command()
def from_subscription():
    (db,) = get_session()
    subscription_repo = SubscriptionRepo(db)
    mautic_repo = MauticRepo()
    for subscription in subscription_repo.list(active=True):
        mautic_repo.process_subscription(subscription)
        click.echo(f"Imported {subscription.id} / {subscription.user.username}")
