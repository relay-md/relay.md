# -*- coding: utf-8 -*-
from backend.utils.document import get_title_from_body


def test_title_extract():
    assert (
        get_title_from_body(
            """
# Example headline
FOobar body
"""
        )
        == "Example headline"
    )
    assert (
        get_title_from_body(
            """



# Example headline
FOobar body
"""
        )
        == "Example headline"
    )

    assert (
        get_title_from_body(
            """
### Example headline
FOobar body
"""
        )
        == "Example headline"
    )
