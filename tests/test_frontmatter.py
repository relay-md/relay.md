# -*- coding: utf-8 -*-
from backend.schema import DocumentFrontMatter


def test_frontmatter_happy_path():
    front = DocumentFrontMatter(**{"relay-to": "foobar"})
    assert front.model_dump().items() >= dict(relay_to=["foobar"]).items()

    front = DocumentFrontMatter(**{"relay-to": ["foobar"]})
    assert front.model_dump().items() >= dict(relay_to=["foobar"]).items()

    front = DocumentFrontMatter(**{"relay_to": "foobar"})
    assert front.model_dump().items() >= dict(relay_to=["foobar"]).items()

    front = DocumentFrontMatter(**{"relay_to": ["foobar"]})
    assert front.model_dump().items() >= dict(relay_to=["foobar"]).items()
