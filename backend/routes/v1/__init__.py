# -*- coding: utf-8 -*-
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Security
from fastapi.security import APIKeyHeader

from ... import exceptions
from ...database import Session, get_session
from ...models.document import Document
from ...models.user import User
from ...repos.access_token import AccessToken, AccessTokenRepo
from ...repos.document import DocumentRepo
from ...repos.user import UserRepo

router = APIRouter(prefix="/v1")

api_key_header = APIKeyHeader(name="X-API-Key")


async def get_access_token(
    api_key_header: str = Security(api_key_header), db: Session = Depends(get_session)
) -> str:
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
    db: Session = Depends(get_session),
    user: User = Depends(optional_authenticated_user),
    document: Document = Depends(get_document),
) -> Document:
    if document.is_public:
        return document
    user_repo = UserRepo(db)
    for team_topic in document.team_topics:
        # TODO: invetigate if we can avoid the loop by a more powerful query
        if user_repo.has_subscribed_to_topic_in_team(user, team_topic):
            return document
    if not user or document.user_id != user.id:
        raise exceptions.NotAllowed(
            "Updating someone else document is not allowed currently!"
        )
    return document


async def get_user_owned_document(
    id: UUID,
    db: Session = Depends(get_session),
    user: User = Depends(require_authenticated_user),
    document: Document = Depends(get_document),
) -> Document:
    if document.user_id != user.id:
        raise exceptions.NotAllowed(
            "Updating someone else document is not allowed currently!"
        )
    return document
