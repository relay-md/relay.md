# -*- coding: utf-8 -*-
from typing import Optional

from fastapi import Depends, Request

from ..database import Session, get_session
from ..repos.user import User


def get_optional_user(
    request: Request, db: Session = Depends(get_session)
) -> Optional[User]:
    from ..repos.user import UserRepo

    user_id = request.session.get("user_id")
    if not user_id:
        return None
    # Returns non in case the user-is invalid
    return UserRepo(db).get_by_id(user_id)


def require_user(
    request: Request, db: Session = Depends(get_session)
) -> Optional[User]:
    from ..exceptions import LoginRequiredException
    from ..repos.user import UserRepo

    user_id = request.session.get("user_id")
    if not user_id:
        # circular dependency here
        raise LoginRequiredException(next_url=request.url)
    # Returns non in case the user-is invalid
    user = UserRepo(db).get_by_id(user_id)
    if not user:
        raise LoginRequiredException(next_url=request.url)
    return user


def require_admin(user: User = Depends(require_user)) -> Optional[User]:
    if not user.is_admin:
        from ..exceptions import NotAllowed

        raise NotAllowed("Only admins can access this area!")
    return user
