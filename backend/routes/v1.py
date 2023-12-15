# -*- coding: utf-8 -*-
import json
from datetime import datetime
from typing import List
from uuid import UUID

import frontmatter
from fastapi import APIRouter, Depends, Request, Security
from fastapi.responses import PlainTextResponse
from fastapi.security import APIKeyHeader

from .. import __version__, exceptions
from ..database import Session, get_session
from ..models.document import Document
from ..models.user import User
from ..repos.access_token import AccessTokenRepo
from ..repos.document import DocumentRepo
from ..repos.document_access import DocumentAccessRepo
from ..repos.document_body import DocumentBodyRepo
from ..repos.user import UserRepo
from ..schema import (
    DocumentFrontMatter,
    DocumentIdentifierResponse,
    DocumentResponse,
    DocumentShareType,
    Response,
    VersionResponse,
)
from ..utils.document import (
    check_document_read_permissions,
    check_document_write_permissions,
    get_shareables,
    get_title_from_body,
)

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
) -> str:
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
    return


async def require_authenticated_user(access_token: str = Security(get_access_token)):
    return access_token.user


async def optional_authenticated_user(
    access_token: str = Security(get_optional_access_token),
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
    # FIXME: here we need to check that the user is subscribed with the team
    # that the document was shared with
    if document.is_public:
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


@router.get(
    "/version",
    tags=["v1"],
    response_model=Response[VersionResponse],
    response_model_exclude_unset=True,
)
async def version():
    return dict(result=dict(version=__version__))


@router.post(
    "/doc",
    tags=["v1"],
    response_model=Response[DocumentResponse],
    response_model_exclude_unset=True,
    response_model_by_alias=True,
)
async def post_doc(
    request: Request,
    filename: str = "",
    user: User = Depends(require_authenticated_user),
    db: Session = Depends(get_session),
):
    document_repo = DocumentRepo(db)
    document_body_repo = DocumentBodyRepo()

    # Get body containing the raw markdown
    body = (await request.body()).decode("utf-8")

    # Parse frontmatter
    front_matter = frontmatter.loads(body)
    front = DocumentFrontMatter(**front_matter)

    if not filename and not front.relay_filename:
        raise exceptions.BadRequest("Missing filename or relay-filename property!")

    # priority of frontmatter
    if front.relay_title:
        title = front.relay_title
    else:
        title = get_title_from_body(front_matter.content)
    if front.relay_filename:
        filename = front.relay_filename

    # At this point we do not allow paths as filename
    if "/" in filename or "\\" in filename:
        raise exceptions.BadRequest("Filenames must not contain slash or backslash")

    # Parse relay_to as team_topics
    shareables = get_shareables(db, front, user)
    check_document_write_permissions(db, user, shareables, "post-document")

    # if the document already has an id, let's raise
    if front.relay_document:
        raise exceptions.BadRequest(
            "The document you are sending already has a relay-document id"
        )

    # Store document in database
    document = document_repo.create_from_kwargs(
        user_id=user.id,
        title=title,
        filename=filename,
        team_topics=shareables.team_topics,
        users=shareables.users,
        is_public=shareables.is_public,
    )

    # Update document content in DocumentBodyRepo
    document_body_repo.create(document.id, body)
    ret_document = DocumentResponse(
        relay_document=document.id,
        relay_title=document.title,
        relay_filename=filename,
        relay_to=front.relay_to,
    )
    return dict(result=ret_document)


@router.get(
    "/doc/{id}",
    tags=["v1"],
)
async def get_doc(
    request: Request,
    document: Document = Depends(get_user_shared_document),
    db: Session = Depends(get_session),
    user: User = Depends(optional_authenticated_user),
):
    check_document_read_permissions(db, user, document.team_topics)
    document_body_repo = DocumentBodyRepo()
    document_access_repo = DocumentAccessRepo(db)
    body = document_body_repo.get_by_id(document.id)

    # Add document id to frontmatter
    front = frontmatter.loads(body)
    front["relay-document"] = str(document.id)
    body = frontmatter.dumps(front)
    if user:
        document_access_repo.create_from_kwargs(
            user_id=user.id, document_id=document.id
        )

    content_type = request.headers.get("content-type", "application/json")
    if content_type == "application/json":
        ret_document = DocumentResponse(
            relay_document=document.id,
            relay_filename=document.filename,
            relay_title=document.title,
            relay_to=document.shared_with,
            body=body,
        )
        return Response(result=ret_document).model_dump(by_alias=True)
    elif content_type == "text/markdown":
        response = PlainTextResponse(body)
        response.headers["X-Relay-document"] = str(document.id)
        response.headers["X-Relay-filename"] = document.filename
        response.headers["X-Relay-to"] = json.dumps(document.shared_with)
        response.headers["X-Relay-title"] = document.title
        return response
    else:
        raise exceptions.BadRequest(f"Unsupported content-type: {content_type}")


@router.put("/doc/{id}", tags=["v1"])
async def put_doc(
    request: Request,
    id: UUID,
    document: Document = Depends(get_user_owned_document),
    user: User = Depends(require_authenticated_user),
    db: Session = Depends(get_session),
):
    document_repo = DocumentRepo(db)
    document_body_repo = DocumentBodyRepo()
    UserRepo(db)

    body = (await request.body()).decode("utf-8")
    front_matter = frontmatter.loads(body)
    front = DocumentFrontMatter(**front_matter)

    if front.relay_title:
        title = front.relay_title
    else:
        title = get_title_from_body(front_matter.content)

    # Parse relay_to as team_topics
    shareables = get_shareables(db, front, user)
    check_document_write_permissions(db, user, shareables, "modify-document")

    document_repo.update(
        document,
        team_topics=shareables.team_topics,
        title=title,
        users=shareables.users,
        is_public=shareables.is_public,
        last_updated_at=datetime.utcnow(),
    )
    # Update document content in DocumentBodyRepo
    document_body_repo.update(document.id, body)
    ret_document = DocumentResponse(
        relay_document=document.id,
        relay_filename=document.filename,
        relay_title=title,
        relay_to=front.relay_to,
        body=body,
    )
    return dict(result=ret_document)


@router.get(
    "/docs",
    tags=["v1"],
    response_model=Response[List[DocumentIdentifierResponse]],
    response_model_exclude_unset=True,
    response_model_by_alias=True,
)
async def get_docs(
    type: str = "all",
    page: int = 0,
    size: int = 50,
    user: User = Depends(require_authenticated_user),
    db: Session = Depends(get_session),
    access_token: str = Security(get_access_token),
):
    document_repo = DocumentRepo(db)
    if type == "mine":
        documents = document_repo.get_my_documents(user, page, size)
    else:
        documents = document_repo.get_shared_documents(
            access_token,
            page,
            size,
            DocumentShareType.PUBLIC
            | DocumentShareType.SHARED_WITH_USER
            | DocumentShareType.SUBSCRIBED_TEAM,
        )
    ret = list()
    for document in documents:
        ret.append(
            DocumentIdentifierResponse(
                relay_document=document.id,
                relay_filename=document.filename,
                relay_to=document.shared_with,
            )
        )
    return dict(result=ret)
