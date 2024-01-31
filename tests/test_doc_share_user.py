# -*- coding: utf-8 -*-
from unittest.mock import patch
from uuid import UUID

import pytest
from sqlalchemy import select

from backend import models

mocked_up_text = """---
relay-filename: example.md
relay-to:
- '@account2'
---

Example text"""


@patch(
    "backend.repos.document_body.DocumentBodyRepo.get_by_id",
    return_value=mocked_up_text.encode("utf-8"),
    autospec=True,
)
def test_document_upload(
    mock,
    account,
    other_account,
    auth_header,
    api_client,
    patch_document_body_create,
    dbsession,
):
    req = api_client.post("/v1/doc", headers=auth_header, content=mocked_up_text)
    req.raise_for_status(), req.text

    ret = req.json()
    doc_id = ret["result"]["relay-document"]

    assert not dbsession.scalar(
        select(models.DocumentAccess).filter_by(
            user_id=account.id, document_id=UUID(doc_id)
        )
    )

    req = api_client.get(f"/v1/doc/{doc_id}", headers=auth_header)
    req.raise_for_status(), req.text

    # check doc has been access
    assert dbsession.scalar(
        select(models.DocumentAccess).filter_by(
            user_id=account.id, document_id=UUID(doc_id)
        )
    )

    # lets add the id to the doc
    original_doc = mocked_up_text.split("\n")
    new_body = "\n".join(
        [original_doc[0], f"relay-document: {doc_id}", *original_doc[1:]]
    )

    ret = req.json()["result"]
    assert ret["relay-document"] == doc_id
    assert ret["relay-to"] == ["@account2"]
    assert ret["relay-filename"] == "example.md"

    req = api_client.get(
        f"/v1/doc/{doc_id}", headers={**auth_header, "content-type": "text/markdown"}
    )
    req.raise_for_status(), req.text
    assert req.text == new_body

    expected = f"""---
relay-document: {doc_id}
relay-filename: example.md
relay-to:
- '@account2'
---
"""
    assert req.text.startswith(expected)
    assert req.headers.get("x-relay-document") == doc_id


def test_document_perms(auth_header, api_client, other_account):
    other_mocked_up_text = """---
relay-document: 8b9a08b5-9fe1-46c3-9d9c-348a42e8bd3f
relay-filename: example.md
relay-to:
- '@account2'
---

Example text
    """
    req = api_client.post("/v1/doc", headers=auth_header, content=other_mocked_up_text)
    req.raise_for_status()
    assert (
        req.json()["error"]["message"]
        == "The document you are sending already has a relay-document id"
    )


def test_document_put(
    other_auth_header,
    auth_header,
    api_client,
    patch_document_body_update,
    patch_document_body_create,
):
    original_doc = """---
relay-filename: example.md
relay-to:
- '@account2'
---

Example text
"""
    req = api_client.post("/v1/doc", headers=auth_header, content=original_doc)
    ret = req.json()
    doc_id = ret["result"]["relay-document"]

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
        f"/v1/doc/{doc_id}", headers=other_auth_header, content=updated_doc
    )
    req.raise_for_status()
    assert (
        req.json()["error"]["message"]
        == "Updating someone else document is not allowed currently!"
    )

    # Now trying to put as correct user
    req = api_client.put(f"/v1/doc/{doc_id}", headers=auth_header, content=updated_doc)
    req.raise_for_status()
    assert req.json()["result"]["relay-document"] == doc_id

    assert "Additional text" in patch_document_body_update.call_args.args[1]
