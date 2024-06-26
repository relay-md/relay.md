# -*- coding: utf-8 -*-
from unittest.mock import patch
from uuid import UUID

from sqlalchemy import select

from backend import models

mocked_up_text = """---
relay-filename: example.md
relay-to:
- mytopic@myteam
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
    auth_header,
    api_client,
    patch_document_body_create,
    dbsession,
):
    req = api_client.post("/v1/doc", headers=auth_header, content=mocked_up_text)
    req.raise_for_status()

    ret = req.json()
    doc_id = ret["result"]["relay-document"]

    assert not dbsession.scalar(
        select(models.DocumentAccess).filter_by(
            user_id=account.id, document_id=UUID(doc_id)
        )
    )

    req = api_client.get(f"/v1/doc/{doc_id}", headers=auth_header)
    req.raise_for_status()

    # check doc has been access
    assert dbsession.scalar(
        select(models.DocumentAccess).filter_by(
            user_id=account.id, document_id=UUID(doc_id)
        )
    )

    document = dbsession.scalar(select(models.Document).filter_by(id=UUID(doc_id)))
    assert not document.is_public

    # lets add the id to the doc
    original_doc = mocked_up_text.split("\n")
    new_body = "\n".join(
        [original_doc[0], f"relay-document: {doc_id}", *original_doc[1:]]
    )

    ret = req.json()["result"]
    assert ret["relay-document"] == doc_id
    assert ret["relay-to"] == ["mytopic@myteam"]
    assert ret["relay-filename"] == "example.md"
    assert ret["relay-title"] == "Example text"

    req = api_client.get(
        f"/v1/doc/{doc_id}", headers={**auth_header, "content-type": "text/markdown"}
    )
    req.raise_for_status()
    assert req.text == new_body

    expected = f"""---
relay-document: {doc_id}
relay-filename: example.md
relay-to:
- mytopic@myteam
---
"""
    assert req.text.startswith(expected)
    assert req.headers.get("x-relay-document") == doc_id


def test_document_perms(auth_header, api_client):
    other_mocked_up_text = """---
relay-document: 8b9a08b5-9fe1-46c3-9d9c-348a42e8bd3f
relay-filename: example.md
relay-to:
- mytopic@myteam
---

Example text
    """
    req = api_client.post("/v1/doc", headers=auth_header, content=other_mocked_up_text)
    req.raise_for_status()
    assert (
        req.json()["error"]["message"]
        == "The document you are sending already has a relay-document id, use PUT instead"
    )
