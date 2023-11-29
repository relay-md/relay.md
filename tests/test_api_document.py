# -*- coding: utf-8 -*-
import json
from unittest.mock import patch

import pytest

mocked_up_text = """---
relay-filename: example.md
relay-to:
 - mytopic@myteam
---

Example text
"""


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
    doc_id = ret["result"]["relay_document"]

    req = api_client.get(f"/v1/doc/{doc_id}", headers=auth_header)
    assert req.ok, req.text

    ret = req.json()["result"]
    assert ret["body"] == mocked_up_text
    assert ret["relay-document"] == doc_id
    assert ret["relay-to"] == ["mytopic@myteam"]
    assert ret["relay-filename"] == "example.md"

    req = api_client.get(
        f"/v1/doc/{doc_id}", headers={**auth_header, "content-type": "text/markdown"}
    )
    assert req.ok, req.text

    assert req.text.startswith(
        """---
relay-filename: example.md
relay-to:
 - mytopic@myteam
---
"""
    )

    assert req.headers.get("x-relay-filename") == "example.md"
    assert req.headers.get("x-relay-document") == doc_id
    assert json.loads(req.headers.get("x-relay-to")) == ["mytopic@myteam"]


def test_document_perms(auth_header, api_client):
    other_mocked_up_text = """---
relay-document: 8b9a08b5-9fe1-46c3-9d9c-348a42e8bd3f
relay-filename: example.md
relay-to:
- mytopic@myteam
---

Example text
    """
    req = api_client.post("/v1/doc", headers=auth_header, data=other_mocked_up_text)
    assert req.status_code == 400
    assert (
        req.json()["error"]["message"]
        == "The document you are sending already has a relay-document id"
    )


def test_document_put(
    other_auth_header, auth_header, api_client, patch_document_body_update
):
    original_doc = """---
relay-filename: example.md
relay-to:
 - mytopic@myteam
---

Example text
"""
    req = api_client.post("/v1/doc", headers=auth_header, data=original_doc)
    ret = req.json()
    doc_id = ret["result"]["relay_document"]

    # lets add the id to the doc
    original_doc_pars = original_doc.split("\n")
    updated_doc = "\n".join(
        [
            original_doc_pars[0],
            f"relay-document: {doc_id}",
            *original_doc_pars[1:],
            "Additional text",
        ]
    )

    # Now trying to put as wrong user
    req = api_client.put(
        f"/v1/doc/{doc_id}", headers=other_auth_header, data=updated_doc
    )
    assert req.status_code == 403
    assert (
        req.json()["error"]["message"]
        == "Updating someone else document is not allowed currently!"
    )

    # Now trying to put as correct user
    req = api_client.put(f"/v1/doc/{doc_id}", headers=auth_header, data=updated_doc)
    assert req.ok
    assert req.json()["result"]["relay-document"] == doc_id

    assert "Additional text" in patch_document_body_update.call_args.args[1].decode(
        "utf-8"
    )
