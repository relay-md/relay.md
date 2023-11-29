# -*- coding: utf-8 -*-
from typing import Optional

from fastapi import Depends, Request

from ..database import Session, get_session
from ..repos.user import User, UserRepo


def get_optional_user(
    request: Request, db: Session = Depends(get_session)
) -> Optional[User]:
    user_id = request.session.get("user_id")
    if not user_id:
        return
    # Returns non in case the user-is invalid
    return UserRepo(db).get_by_id(user_id)
