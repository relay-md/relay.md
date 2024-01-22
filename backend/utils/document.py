# -*- coding: utf-8 -*-
import re
from collections import namedtuple
from typing import List

from .. import exceptions
from ..database import Session
from ..models.permissions import Permissions
from ..models.team_topic import TeamTopic
from ..models.user import User
from ..repos.team_topic import TeamTopicRepo
from ..repos.user import UserRepo
from ..schema import DocumentFrontMatter

Shareables = namedtuple("Shareables", "team_topics users is_public")


def get_title_from_body(body: str) -> str:
    """Return the title of a document given the body"""
    match = re.search("^#+\s+(.*)", body, re.MULTILINE)  # noqa
    if match:
        return match.group(1)
    lines = body.split("\n")
    # else return the first line that is not empty

    def line_allowed_for_headline(line: str) -> bool:
        if len(line) < 1:
            return False
        if line.startswith("---"):
            return False
        return True

    try:
        return next(filter(line_allowed_for_headline, lines))
    except StopIteration:
        return "unknown"


def check_document_read_permissions(
    db: Session, user: User, team_topics: List[TeamTopic]
):
    user_repo = UserRepo(db)
    for team_topic in team_topics:
        team = team_topic.team
        membership = user_repo.is_member(user, team_topic.team)

        if not team.can(Permissions.can_post, user, membership):
            raise exceptions.NotAllowed(
                f"You are not allowed to read from {team_topic.team}!"
            )


def check_document_post_permissions(db: Session, user: User, shareables: Shareables):
    user_repo = UserRepo(db)
    for team_topic in shareables.team_topics:
        team = team_topic.team
        membership = user_repo.is_member(user, team_topic.team)

        if not team.can(Permissions.can_post, user, membership):
            raise exceptions.NotAllowed(
                f"You are not allowed to post to {team_topic.team}!"
            )


def check_document_modify_permissions(db: Session, user: User, shareables: Shareables):
    user_repo = UserRepo(db)
    for team_topic in shareables.team_topics:
        team = team_topic.team
        membership = user_repo.is_member(user, team_topic.team)

        if not team.can(Permissions.can_modify, user, membership):
            raise exceptions.NotAllowed(
                f"You are not allowed to modify posts in {team_topic.team}!"
            )


def get_shareables(db: Session, front: DocumentFrontMatter, user: User) -> Shareables:
    """Is used on POST and PUT.
    Converts string version of relay-to into team_topic instances or user
    instance.
    """
    user_repo = UserRepo(db)
    team_topic_repo = TeamTopicRepo(db)
    team_topics = list()
    users = list()
    is_public = False
    for to in front.relay_to:
        if to.startswith("@"):
            to_user = user_repo.get_by_kwargs(username=to[1:])
            if not to_user:
                raise exceptions.BadRequest(f"User {to} does not exist")
            users.append(to_user)
        else:
            # WARNING: If any of the targets is non-private, the entire document
            # becomes public!
            if "@" not in to:
                continue
            topic, team = to.split("@")
            team_topic = team_topic_repo.from_string(to, user)
            if team_topic.team.public_permissions & Permissions.can_read:
                is_public = True
            team_topics.append(team_topic)
    return Shareables(team_topics=team_topics, users=users, is_public=is_public)
