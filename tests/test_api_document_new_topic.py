# -*- coding: utf-8 -*-
import json
from unittest.mock import patch

import pytest

mocked_up_text = """---
relay-filename: example.md
relay-to:
- mytopic@myteam
- newtopic@myteam
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


@pytest.fixture
def patch_document_body_update():
    with patch(
        "backend.repos.document_body.DocumentBodyRepo.update",
    ) as mock:
        yield mock


@pytest.fixture
def s3(patch_document_body_create, patch_document_body_get):
    yield


def test_document_upload(auth_header, api_client, s3):
    req = api_client.post("/v1/doc", headers=auth_header, data=mocked_up_text)
    assert req.ok, req.text

    ret = req.json()
    doc_id = ret["result"]["relay-document"]

    req = api_client.get(f"/v1/doc/{doc_id}", headers=auth_header)
    assert req.ok, req.text

    # lets add the id to the doc
    original_doc = mocked_up_text.split("\n")
    new_body = "\n".join(
        [original_doc[0], f"relay-document: {doc_id}", *original_doc[1:]]
    )

    ret = req.json()["result"]
    assert ret["body"] == new_body
    assert ret["relay-document"] == doc_id
    assert ret["relay-to"] == ["mytopic@myteam", "newtopic@myteam"]
    assert ret["relay-filename"] == "example.md"

    req = api_client.get(
        f"/v1/doc/{doc_id}", headers={**auth_header, "content-type": "text/markdown"}
    )
    assert req.ok, req.text

    expected = f"""---
relay-document: {doc_id}
relay-filename: example.md
relay-to:
- mytopic@myteam
- newtopic@myteam
---
"""
    assert req.text.startswith(expected)
    assert req.headers.get("x-relay-filename") == "example.md"
    assert req.headers.get("x-relay-document") == doc_id
    assert json.loads(req.headers.get("x-relay-to")) == [
        "mytopic@myteam",
        "newtopic@myteam",
    ]


def test_document_upload_invalid_team(auth_header, api_client):
    mocked_up_text = """---
relay-filename: example.md
relay-to:
- mytopic@myteam
- newtopic@invalid
---

Example text"""
    req = api_client.post("/v1/doc", headers=auth_header, data=mocked_up_text)
    assert req.ok
    assert req.json()["error"]["message"] == "Team 'invalid' does not exist!"