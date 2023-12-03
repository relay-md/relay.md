# -*- coding: utf-8 -*-
from typing import List

import pytest


@pytest.fixture
def create_document(account, team_topic_repo, user_repo, document_repo):
    def func(
        filename: str,
        team_topics: List[str] = [],
        users: List[str] = [],
        is_public: bool = False,
    ):
        tts = list()
        for tt_name in team_topics:
            tts.append(team_topic_repo.from_string(tt_name))
        us = list()
        for user in users:
            us.append(user_repo.from_string(user))
        return document_repo.create_from_kwargs(
            filename=filename,
            team_topics=tts,
            user_id=account.id,
            users=us,
            is_public=is_public,
        )

    yield func


@pytest.fixture
def subscribe_to_team_topic(account, team_topic_repo, user_team_topic_repo):
    def func(acc, team_topic: str):
        t = team_topic_repo.from_string(team_topic)
        return user_team_topic_repo.create_from_kwargs(
            team_topic_id=t.id,
            user_id=acc.id,
        )

    yield func


def test_get_docs_no_subscription(
    account, auth_header, api_client, dbsession, create_document
):
    req = api_client.get("/v1/docs", headers=auth_header)
    assert req.ok
    assert req.json()["result"] == []


def test_get_docs_just_shared_with_me(
    account,
    other_account,
    eve_auth_header,
    other_auth_header,
    auth_header,
    api_client,
    dbsession,
    create_document,
):
    document = create_document("foo.bar.text", [], [other_account.username], False)
    req = api_client.get("/v1/docs", headers=other_auth_header)
    assert req.ok
    assert len(req.json()["result"]) == 1
    ret_doc = req.json()["result"][0]
    ret_doc["relay-document"] == str(document.id)

    # not shared with me though :D
    req = api_client.get("/v1/docs", headers=eve_auth_header)
    assert req.ok
    assert len(req.json()["result"]) == 0


def test_get_docs_in_team_topics_i_subscribed(
    account,
    other_account,
    eve_auth_header,
    other_auth_header,
    auth_header,
    api_client,
    dbsession,
    create_document,
    create_team,
    create_team_topic,
    subscribe_to_team_topic,
):
    create_team("test", allow_create_topics=True)
    team_topic = create_team_topic("unit@test")
    document = create_document("foo.bar.text", [team_topic.name], [], False)
    req = api_client.get("/v1/docs", headers=auth_header)
    assert req.ok
    assert len(req.json()["result"]) == 0

    # No we subscribe and try again
    subscribe_to_team_topic(account, team_topic.name)
    req = api_client.get("/v1/docs", headers=auth_header)
    assert req.ok
    assert len(req.json()["result"]) == 1
    ret_doc = req.json()["result"][0]
    ret_doc["relay-document"] == str(document.id)


def test_cannot_subscribe_private_team(
    account,
    other_account,
    eve_auth_header,
    other_auth_header,
    auth_header,
    api_client,
    dbsession,
    create_team,
    create_team_topic,
    subscribe_to_team_topic,
):
    create_team("test", allow_create_topics=True, is_private=True)
    create_team_topic("unit@test")

    # No we subscribe and try again
