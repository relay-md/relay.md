# -*- coding: utf-8 -*-
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Security
from fastapi.security import APIKeyHeader

from ... import exceptions
from ...database import Session, get_session
from ...models.document import Document
from ...models.permissions import Permissions
from ...models.user import User
from ...repos.access_token import AccessToken, AccessTokenRepo
from ...repos.document import DocumentRepo
from ...repos.user import UserRepo
from ...repos.user_team import UserTeamRepo
from ...utils.document import Shareables

router = APIRouter(prefix="/v1")

api_key_header = APIKeyHeader(name="X-API-Key")


async def get_access_token(
    api_key_header: str = Security(api_key_header), db: Session = Depends(get_session)
) -> AccessToken:
    try:
        api_key_uuid = UUID(api_key_header)
        access_token_repo = AccessTokenRepo(db)
        access_token = access_token_repo.get_by_id(api_key_uuid)
        if access_token:
            return access_token
    except Exception:
        pass
    raise exceptions.Unauthorized("Invalid or missing API Key")


async def get_optional_access_token(
    api_key_header: str = Security(api_key_header), db: Session = Depends(get_session)
) -> Optional[str]:
    """This still requires that the X-API-key is defined in the header"""
    try:
        api_key_uuid = UUID(api_key_header)
        access_token_repo = AccessTokenRepo(db)
        access_token = access_token_repo.get_by_id(api_key_uuid)
        if access_token:
            return access_token
    except Exception:
        pass
    # We need this optional autentication to be able to share documents
    # without requiring a login
    return None


async def require_authenticated_user(
    access_token: AccessToken = Security(get_access_token),
):
    return access_token.user


async def optional_authenticated_user(
    access_token: AccessToken = Security(get_optional_access_token),
):
    """We need this optional autentication to be able to share documents
    without requiring a login
    """
    if access_token:
        return access_token.user


async def get_document(id: UUID, db: Session = Depends(get_session)) -> Document:
    document_repo = DocumentRepo(db)
    document = document_repo.get_by_id(id)
    if not document:
        raise exceptions.NotFound("document id unknown")
    return document


async def get_user_shared_document(
    id: UUID,
    permission: Permissions,
    db: Session,
    user: User,
    document: Document,
) -> Document:
    # Lets go through the team/topics and check perms individually
    UserRepo(db)
    if user and document.user_id == user.id:
        return document
    user_team_repo = UserTeamRepo(db)
    for team_topic in document.team_topics:
        membership = user_team_repo.get_by_kwargs(
            user_id=user.id, team_id=team_topic.team_id
        )
        if team_topic.team.can(permission, user, membership):
            return document
    raise exceptions.NotAllowed("You are not allowed to do what you are trying to do!")


async def get_user_shared_document_for_read(
    id: UUID,
    db: Session = Depends(get_session),
    user: User = Depends(optional_authenticated_user),
    document: Document = Depends(get_document),
) -> Document:
    # Everyone can read public documents
    if document.is_public:
        return document

    return await get_user_shared_document(id, Permissions.can_read, db, user, document)


async def get_user_shared_document_for_modify(
    id: UUID,
    db: Session = Depends(get_session),
    user: User = Depends(optional_authenticated_user),
    document: Document = Depends(get_document),
) -> Document:
    return await get_user_shared_document(
        id, Permissions.can_modify, db, user, document
    )


async def get_user_owned_document(
    id: UUID,
    db: Session = Depends(get_session),
    user: User = Depends(require_authenticated_user),
    document: Document = Depends(get_document),
) -> Document:
    if document.user_id != user.id:
        raise exceptions.NotAllowed(
            "Deleting someone else's document is not allowed currently!"
        )
    return document


def check_document_post_permissions(db: Session, user: User, shareables: Shareables):
    user_repo = UserRepo(db)
    for team_topic in shareables.team_topics:
        team = team_topic.team
        membership = user_repo.is_member(user, team_topic.team)

        if team.can(Permissions.can_post, user, membership):
            return
    # If we have team_topics and we get to this point, we need to raise
    if shareables.team_topics:
        raise exceptions.NotAllowed("You are not allowed!")
