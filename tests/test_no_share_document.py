# -*- coding: utf-8 -*-
from unittest.mock import patch
from uuid import UUID

import pytest


@pytest.fixture(autouse=True)
def patch_document_body_create():
    with patch("backend.repos.document_body.DocumentBodyRepo.create") as mock:
        yield mock


def test_public_post(
    eve_auth_header,
    upload_document,
):
    document = upload_document("foobar", eve_auth_header, None)
    assert UUID(document["relay-document"])
