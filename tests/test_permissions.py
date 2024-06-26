# -*- coding: utf-8 -*-
from unittest.mock import patch

import pytest

from backend.exceptions import NotAllowed
from backend.models.team import DEFAULT_PUBLIC_PERMISSIONS, Permissions


@patch(
    "backend.repos.document_body.DocumentBodyRepo.get_by_id",
    autospec=True,
)
def test_public_create_team_topic(
    mock,
    dbsession,
    create_team,
    create_team_topic,
    eve,
    patch_document_body_create,
    patch_document_body_update,
):
    team = create_team(
        "public-test", public_permissions=DEFAULT_PUBLIC_PERMISSIONS.value
    )
    create_team_topic("testing@public-test", eve)

    team.public_permissions = (
        DEFAULT_PUBLIC_PERMISSIONS & ~Permissions.can_create_topics
    )
    dbsession.commit()

    with pytest.raises(NotAllowed):
        create_team_topic("testing-2@public-test", eve)


@patch(
    "backend.repos.document_body.DocumentBodyRepo.get_by_id",
    autospec=True,
)
def test_public_post(
    mock,
    dbsession,
    eve_auth_header,
    auth_header,
    create_team,
    upload_document,
    patch_document_body_create,
    patch_document_body_update,
):
    team = create_team(
        "public-test",
        public_permissions=DEFAULT_PUBLIC_PERMISSIONS & Permissions.can_post,
    )
    upload_document("foobar", auth_header, "testing@public-test")
    upload_document("foobar", eve_auth_header, "testing@public-test")

    team.public_permissions = DEFAULT_PUBLIC_PERMISSIONS & ~Permissions.can_post
    dbsession.commit()

    upload_document("foobar", auth_header, "testing@public-test")
    with pytest.raises(ValueError) as exc:
        upload_document("foobar", eve_auth_header, "testing@public-test")
    assert exc.value.args[0] == 403
    assert exc.value.args[1].startswith("You are not allowed!")


@patch(
    "backend.repos.document_body.DocumentBodyRepo.get_by_id",
    autospec=True,
)
def test_public_modify(
    mock,
    dbsession,
    other_account,
    eve_auth_header,
    auth_header,
    create_team,
    upload_document,
    update_document,
    patch_document_body_create,
    patch_document_body_update,
):
    create_team(
        "public-test",
        public_permissions=(DEFAULT_PUBLIC_PERMISSIONS & ~Permissions.can_modify),
        user_id=other_account.id,
    )
    document = upload_document("foobar", eve_auth_header, "testing@public-test")

    update_document(
        document["relay-document"], "foobar2", eve_auth_header, "testing@public-test"
    )
    with pytest.raises(ValueError) as exc:
        # some other dude cannot modify our document!
        update_document(
            document["relay-document"],
            "foobar3",
            auth_header,
            "testing@public-test",
        )
    assert exc.value.args[0] == 403
    assert exc.value.args[1].startswith(
        "You are not allowed to do what you are trying to do!"
    )
