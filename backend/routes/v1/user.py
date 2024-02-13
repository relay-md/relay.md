# -*- coding: utf-8 -*-

from fastapi import Depends

from ...models.user import User
from ...schema import Response, UserResponse
from . import require_authenticated_user, router


@router.get(
    "/user",
    tags=["v1"],
    response_model=Response[UserResponse],
)
async def get_user(
    user: User = Depends(require_authenticated_user),
):
    return dict(result=user)
