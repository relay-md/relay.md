# -*- coding: utf-8 -*-
from backend.models.team import (
    DEFAULT_MEMBER_PERMISSIONS,
    DEFAULT_PUBLIC_PERMISSIONS,
    Permissions,
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
 - mytopic@myteam
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

    # Now trying to put as correct user
    req = api_client.put(f"/v1/doc/{doc_id}", headers=auth_header, content=updated_doc)
    req.raise_for_status()
    assert req.json()["result"]["relay-document"] == doc_id
    assert req.json()["result"]["relay-title"] == "Example text"

    assert "Additional text" in patch_document_body_update.call_args.args[1]


def test_not_allow_modify_public(
    create_team,
    create_team_topic,
    create_document,
    other_auth_header,
    api_client,
):
    create_team(
        "test",
        public_permissions=(DEFAULT_PUBLIC_PERMISSIONS & ~Permissions.can_modify),
    )
    team_topic = create_team_topic("test@test")
    document = create_document("foobar.md", ["test@test"])

    assert document.team_topics[0].id == team_topic.id
    # Now trying to put as wrong user
    req = api_client.put(
        f"/v1/doc/{document.id}", headers=other_auth_header, content=""
    )
    req.raise_for_status()
    assert (
        req.json()["error"]["message"]
        == "You are not allowed to do what you are trying to do!"
    )


def test_allow_modify_by_public(
    create_team,
    create_team_topic,
    create_document,
    other_auth_header,
    api_client,
    patch_document_body_update,
    patch_document_body_create,
):
    create_team(
        "test",
        public_permissions=(DEFAULT_PUBLIC_PERMISSIONS | Permissions.can_modify),
    )
    team_topic = create_team_topic(
        "test@test",
    )
    document = create_document("foobar.md", ["test@test"])

    assert document.team_topics[0].id == team_topic.id
    # Now trying to put as wrong user
    new_content = """---
relay-filename: example.md
relay-to:
 - mytopic@myteam
---

Example text
"""
    req = api_client.put(
        f"/v1/doc/{document.id}", headers=other_auth_header, content=new_content
    )
    req.raise_for_status()
    assert "error" not in req.json()


def test_allow_read_by_member(
    create_team,
    create_team_topic,
    create_document,
    other_account,
    other_auth_header,
    api_client,
    join_team,
):
    team = create_team("test", public_permissions=0)
    team_topic = create_team_topic(
        "test@test",
    )
    document = create_document("foobar.md", ["test@test"])
    join_team(
        team,
        other_account,
        permissions=DEFAULT_MEMBER_PERMISSIONS | Permissions.can_read,
    )
    assert document.team_topics[0].id == team_topic.id
    req = api_client.get(f"/v1/doc/{document.id}", headers=other_auth_header)
    req.raise_for_status()
    assert "error" not in req.json()


def test_not_allow_modify_by_member(
    create_team,
    create_team_topic,
    create_document,
    other_account,
    other_auth_header,
    api_client,
    join_team,
):
    team = create_team("test", public_permissions=0)
    team_topic = create_team_topic(
        "test@test",
    )
    document = create_document("foobar.md", ["test@test"])
    join_team(
        team,
        other_account,
        permissions=DEFAULT_MEMBER_PERMISSIONS & ~Permissions.can_modify,
    )
    assert document.team_topics[0].id == team_topic.id
    req = api_client.put(
        f"/v1/doc/{document.id}", headers=other_auth_header, content=""
    )
    req.raise_for_status()
    assert (
        req.json()["error"]["message"]
        == "You are not allowed to do what you are trying to do!"
    )


def test_allow_modify_by_member(
    create_team,
    create_team_topic,
    create_document,
    other_account,
    other_auth_header,
    api_client,
    join_team,
    patch_document_body_update,
    patch_document_body_create,
):
    team = create_team("test", public_permissions=0)
    team_topic = create_team_topic(
        "test@test",
    )
    document = create_document("foobar.md", ["test@test"])
    join_team(
        team,
        other_account,
        permissions=DEFAULT_MEMBER_PERMISSIONS | Permissions.can_modify,
    )
    assert document.team_topics[0].id == team_topic.id
    # Now trying to put as wrong user
    new_content = """---
relay-filename: example.md
relay-to:
 - mytopic@myteam
---

Example text
"""
    req = api_client.put(
        f"/v1/doc/{document.id}", headers=other_auth_header, content=new_content
    )
    req.raise_for_status()
    assert "error" not in req.json()
