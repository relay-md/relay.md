# -*- coding: utf-8 -*-

import pytest
from unittest.mock import patch
from uuid import UUID
from sqlalchemy import select

from backend import models


def test_document_upload(
    account,
    auth_header,
    api_client,
    dbsession,
    patch_document_body_create,
    other_auth_header,
):
    mocked_up_text = """---
relay-filename: example.md
relay-to:
- mytopic@_
---

Example text"""
    req = api_client.post("/v1/doc", headers=auth_header, content=mocked_up_text)
    req.raise_for_status()

    ret = req.json()
    doc_id = ret["result"]["relay-document"]

    document = dbsession.scalar(select(models.Document).filter_by(id=UUID(doc_id)))
    assert document.is_public

    # Need a valid auth header, but can be of anyone
    req = api_client.get(f"/v1/doc/{doc_id}", headers=other_auth_header)
    req.raise_for_status()


def test_document_upload_str_instead_of_list(
    account,
    auth_header,
    api_client,
    dbsession,
    patch_document_body_create,
    other_auth_header,
):
    mocked_up_text = """---
relay-filename: example.md
relay-to: mytopic@_
---

Example text"""
    req = api_client.post("/v1/doc", headers=auth_header, content=mocked_up_text)
    req.raise_for_status()

    ret = req.json()
    doc_id = ret["result"]["relay-document"]

    document = dbsession.scalar(select(models.Document).filter_by(id=UUID(doc_id)))
    assert document.team_topics
    assert document.team_topics[0].name == "mytopic@_"
    assert document.is_public

    # Need a valid auth header, but can be of anyone
    req = api_client.get(f"/v1/doc/{doc_id}", headers=other_auth_header)
    req.raise_for_status()
