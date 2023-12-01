# -*- coding: utf-8 -*-
from unittest.mock import patch
from uuid import UUID

import pytest
from sqlalchemy import select

from backend import models

mocked_up_text = """---
relay-filename: example.md
relay-to:
- mytopic@_
---

Example text"""


@pytest.fixture
def patch_document_body_create():
    with patch("backend.repos.document_body.DocumentBodyRepo.create") as mock:
        yield mock


@pytest.fixture
def patch_document_body_get():
    with patch(
        "backend.repos.document_body.DocumentBodyRepo.get_by_id",
        return_value=mocked_up_text,
    ):
        yield


def test_document_upload(
    account,
    auth_header,
    api_client,
    dbsession,
    patch_document_body_create,
    other_auth_header,
    patch_document_body_get,
):
    req = api_client.post("/v1/doc", headers=auth_header, data=mocked_up_text)
    assert req.ok, req.text

    ret = req.json()
    doc_id = ret["result"]["relay_document"]

    document = dbsession.scalar(select(models.Document).filter_by(id=UUID(doc_id)))
    assert document.is_public

    # Need a valid auth header, but can be of anyone
    req = api_client.get(f"/v1/doc/{doc_id}", headers=other_auth_header)
    assert req.ok
