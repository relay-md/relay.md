# -*- coding: utf-8 -*-
import re


def get_title_from_body(body: str) -> str:
    """Return the title of a document given the body"""
    match = re.search("^#+\s+(.*)", body, re.MULTILINE)  # noqa
    if match:
        return match.group(1)
    lines = body.split("\n")
    # else return the first line that is not empty

    def line_allowed_for_headline(line: str) -> bool:
        if len(line) < 1:
            return False
        if line.startswith("---"):
            return False
        return True

    return next(filter(line_allowed_for_headline, lines))
