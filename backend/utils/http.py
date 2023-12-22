# -*- coding: utf-8 -*-

import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from ..config import get_config

security = HTTPBasic()


def required_basic_auth(credentials: HTTPBasicCredentials = Depends(security)):
    forbidden = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect credentials",
        headers={"WWW-Authenticate": "Basic"},
    )
    allowed = get_config().PAYMENT_BASIC_AUTH_WHITELIST
    allowed_set = list(filter(lambda x: x[0] == credentials.username, allowed))
    if not allowed_set:
        raise forbidden
    allowed_set = allowed_set[0]
    credentials.password.encode("utf8")
    if not secrets.compare_digest(
        credentials.password.encode("utf8"), allowed_set[1].encode("utf8")
    ):
        raise forbidden
    return credentials.username
