# -*- coding: utf-8 -*-
from uuid import UUID

import frontmatter
from fastapi import APIRouter, Depends, Request
from fastapi import Response as FastAPIResponse
from fastapi import Security
from fastapi.responses import PlainTextResponse
from fastapi.security import APIKeyHeader

from .. import exceptions
from ..database import Session, get_session
from ..models.document import Document
from ..models.user import User
from ..repos.access_token import AccessTokenRepo
from ..repos.document import DocumentRepo
from ..repos.document_body import DocumentBodyRepo
from ..repos.team_topic import TeamTopicRepo
from ..schema import DocumentFrontMatter, DocumentResponse, Response

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


async def authenticated_user(access_token: str = Security(get_access_token)):
    return access_token.user


async def get_document(id: UUID, db: Session = Depends(get_session)) -> Document:
    document_repo = DocumentRepo(db)
    document = document_repo.get_by_id(id)
    if not document:
        raise exceptions.NotFound("document id unknown")
    return document


async def get_user_owned_document(
    user: User = Depends(authenticated_user),
    document: Document = Depends(get_document),
):
    if document.user_id != user.id:
        raise exceptions.NotAllowed("This is not your document")


@router.post(
    "/doc",
    tags=["v1"],
    response_model=Response[DocumentResponse],
    response_model_exclude_unset=True,
)
async def post_doc(
    filename: str,
    request: Request,
    user: User = Depends(authenticated_user),
    db: Session = Depends(get_session),
):
    team_topic_repo = TeamTopicRepo(db)
    document_repo = DocumentRepo(db)
    document_body_repo = DocumentBodyRepo()

    # Get body containing the raw markdown
    body = await request.body()

    # Parse frontmatter
    front = DocumentFrontMatter(**frontmatter.loads(body.decode("utf-8")))

    # Parse relay_to as team_topics
    team_topics = list()
    for team_topic in front.relay_to:
        team_topics.append(team_topic_repo.from_string(team_topic))

    # Store document in database
    document = Document(user_id=user.id, filename=filename, team_topics=team_topics)
    document_repo.create(document)

    # Update document content in DocumentBodyRepo
    document_body_repo.create(document.id, body)
    return dict(result=document)


@router.get(
    "/doc/{id}",
    tags=["v1"],
)
async def get_doc(
    request: Request,
    response: FastAPIResponse,
    document: Document = Depends(get_document),
):
    if document.is_private:
        raise exceptions.NotAllowed("Access to this document is not allowed for you.")
    document_body_repo = DocumentBodyRepo()
    body = document_body_repo.get_by_id(document.id)

    content_type = request.headers.get("content-type", "application/json")
    if content_type == "application/json":
        ret_document = DocumentResponse(
            id=document.id,
            filename=document.filename,
            team_topics=document.team_topics,
            body=body,
        )
        return Response(result=ret_document)
    elif content_type == "text/markdown":
        response.headers["X-Relay-filename"] = document.filename
        response.headers["X-Relay-ruid"] = str(document.id)
        return PlainTextResponse(body)
    else:
        raise exceptions.BadRequest(f"Unsupported content-type: {content_type}")


@router.put("/doc/{id}", tags=["v1"])
async def put_doc(
    request: Request, id: UUID, document: Document = Depends(get_user_owned_document)
):
    raise NotImplementedError("This functionatlity is not implemented yet!")
