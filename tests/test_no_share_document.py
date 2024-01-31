# -*- coding: utf-8 -*-
from uuid import UUID


def test_public_post(eve_auth_header, upload_document, patch_document_body_create):
    document = upload_document("foobar", eve_auth_header, None)
    assert UUID(document["relay-document"])
