# -*- coding: utf-8 -*-
""" The methods in this file help us deal with various redirects during login,
authentication or registration procedures. They build a stack so that the
redirect would go to the last element in the stack and proceed from there. This
is needed in case we add 2FA or advanced onboarding etc.
"""
from typing import Optional

from fastapi import Request


def get_next_url(req: Request) -> Optional[str]:
    if "next" not in req.session:
        return
    try:
        return req.session["next"].pop()
    except IndexError:
        return


def add_next_url(req: Request, url: Optional[str]):
    if not url:
        return
    if "next" not in req.session:
        req.session["next"] = []
    # no duplicates in next-stack
    if url not in req.session["next"]:
        req.session["next"].append(url)
