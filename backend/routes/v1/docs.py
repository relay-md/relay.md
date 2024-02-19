# -*- coding: utf-8 -*-
import hashlib
from datetime import datetime
from typing import List

import frontmatter
from fastapi import Depends, Request, Security
from fastapi.responses import PlainTextResponse

from backend.repos.team_topic import TeamTopicRepo
from backend.repos.user_team_topic import UserTeamTopicRepo

from ... import __version__, exceptions
from ...database import Session, get_session
from ...models.access_token import AccessToken
from ...models.document import Document
from ...models.user import User
from ...repos.document import DocumentRepo
from ...repos.document_access import DocumentAccessRepo
from ...repos.document_body import DocumentBodyRepo
from ...repos.user import UserRepo
from ...schema import (
    DocumentFrontMatter,
    DocumentIdentifierResponse,
    DocumentLibraryResponse,
    DocumentResponse,
    DocumentShareType,
    Response,
    VersionResponse,
)
from ...utils.document import (
    check_document_modify_permissions,
    check_document_post_permissions,
    check_document_read_permissions,
    get_shareables,
    get_title_from_body,
)
from . import (
    get_access_token,
    get_user_owned_document,
    get_user_shared_document,
    optional_authenticated_user,
    require_authenticated_user,
    router,
)


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
    body_raw = await request.body()
    body = body_raw.decode("utf-8")

    # Parse frontmatter
    front_matter = frontmatter.loads(body)

    # reformat frontmatter
    front = DocumentFrontMatter(**front_matter)

    """
    # TODO: this code would make things cleaner but breaks the plugin!
    # Add the front mattter attributes the way they should be
    for k, v in front.model_dump(by_alias=True).items():
        if v:
            front_matter[k] = v
    # Remove the version that shouldn't be used
    for k in front.model_dump(by_alias=False):
        front_matter.metadata.pop(k, None)
    # store the updated body
    body = frontmatter.dumps(front_matter)
    """

    if not filename and not front.relay_filename:
        raise exceptions.BadRequest("Missing filename or relay-filename property!")

    # priority of frontmatter
    if front.relay_title:
        title = front.relay_title
    else:
        title = get_title_from_body(front_matter.content)
    if front.relay_filename:
        filename = front.relay_filename

    # Parse relay_to as team_topics
    shareables = get_shareables(db, front, user)
    check_document_post_permissions(db, user, shareables)

    # if the document already has an id, let's raise
    if front.relay_document:
        raise exceptions.BadRequest(
            "The document you are sending already has a relay-document id, use PUT instead"
        )

    # Checksum
    hashing_obj = hashlib.sha256()
    hashing_obj.update(body_raw)
    sha256 = hashing_obj.hexdigest()

    # Store document in database
    document = document_repo.create_from_kwargs(
        user_id=user.id,
        title=title,
        filename=filename,
        team_topics=shareables.team_topics,
        users=shareables.users,
        is_public=shareables.is_public,
        filesize=len(body),
        checksum_sha256=sha256,
    )

    # Update document content in DocumentBodyRepo
    document_body_repo.create(document.id, body)
    ret_document = DocumentResponse(
        relay_document=document.id,
        relay_title=document.title,
        relay_filename=filename,
        relay_to=front.relay_to,
        checksum_sha256=document.checksum_sha256,
        filesize=document.filesize,
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
    if not document.is_public:
        check_document_read_permissions(db, user, document.team_topics)
    document_body_repo = DocumentBodyRepo()
    document_access_repo = DocumentAccessRepo(db)

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
            checksum_sha256=document.checksum_sha256,
            filesize=document.filesize,
            embeds=document.embeds,
        )
        return Response(result=ret_document).model_dump(by_alias=True)
    elif content_type == "text/markdown":
        # Add document id to frontmatter
        body = document_body_repo.get_by_id(document.id)
        body = body.decode("utf-8")
        front = frontmatter.loads(body)
        front["relay-document"] = str(document.id)
        body = frontmatter.dumps(front)

        response = PlainTextResponse(body)
        response.headers["X-Relay-document"] = str(document.id)
        return response
    else:
        raise exceptions.BadRequest(f"Unsupported content-type: {content_type}")


@router.put("/doc/{id}", tags=["v1"])
async def put_doc(
    request: Request,
    document: Document = Depends(get_user_owned_document),
    user: User = Depends(require_authenticated_user),
    db: Session = Depends(get_session),
):
    document_repo = DocumentRepo(db)
    document_body_repo = DocumentBodyRepo()
    UserRepo(db)

    body_raw = await request.body()
    body = body_raw.decode("utf-8")

    front_matter = frontmatter.loads(body)
    front = DocumentFrontMatter(**front_matter)

    if front.relay_title:
        title = front.relay_title
    else:
        title = get_title_from_body(front_matter.content)

    # Parse relay_to as team_topics
    shareables = get_shareables(db, front, user)
    check_document_modify_permissions(db, user, shareables)

    # Checksum
    hashing_obj = hashlib.sha256()
    hashing_obj.update(body_raw)
    sha256 = hashing_obj.hexdigest()

    if sha256 != document.checksum_sha256:
        # We skip the update when the doucment hasn't changed!
        document = document_repo.update(
            document,
            team_topics=shareables.team_topics,
            title=title,
            users=shareables.users,
            is_public=shareables.is_public,
            last_updated_at=datetime.utcnow(),
            filesize=len(body),
            checksum_sha256=sha256,
        )
        # Update document content in DocumentBodyRepo
        document_body_repo.update(document.id, body)

    ret_document = DocumentResponse(
        relay_document=document.id,
        relay_filename=document.filename,
        relay_title=title,
        relay_to=front.relay_to,
        checksum_sha256=document.checksum_sha256,
        filesize=document.filesize,
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
    access_token: AccessToken = Security(get_access_token),
):
    document_repo = DocumentRepo(db)
    if type == "mine":
        documents = document_repo.get_my_documents(user, page, size)
    else:
        documents = document_repo.get_shared_documents(
            access_token,
            page,
            size,
            DocumentShareType.SHARED_WITH_USER | DocumentShareType.SUBSCRIBED_TEAM,
        )
    ret = list()
    for document in documents:
        ret.append(
            DocumentIdentifierResponse(
                relay_document=document.id,
                relay_filename=document.filename,
                relay_to=document.shared_with,
                checksum_sha256=document.checksum_sha256,
            )
        )
    return dict(result=ret)


@router.get(
    "/docs/{team_topic_name}",
    tags=["v1"],
    response_model=Response[List[DocumentLibraryResponse]],
    response_model_exclude_unset=True,
    response_model_by_alias=True,
)
async def get_team_topic_docs(
    request: Request,
    team_topic_name: str,
    type: str = "all",
    page: int = 0,
    size: int = 50,
    user: User = Depends(require_authenticated_user),
    db: Session = Depends(get_session),
):
    team_topic = TeamTopicRepo(db).from_string(team_topic_name, user)
    if not team_topic:
        raise exceptions.NotFound("Invalid Topic")
    user_team_topic = UserTeamTopicRepo(db).get_by_kwargs(
        team_topic_id=team_topic.id, user_id=user.id
    )
    if not user_team_topic:
        raise exceptions.NotFound("Not Subscribed to topic")
    document_repo = DocumentRepo(db)
    ret = list()
    documents = document_repo.list_from_team_topic(team_topic, size, page)
    for document in documents:
        ret.append(
            DocumentLibraryResponse(
                relay_document=document.id,
                relay_filename=document.filename,
                relay_to=document.shared_with,
                checksum_sha256=document.checksum_sha256,
                author=document.user,
                title=document.title,
                last_updated_at=document.last_updated_at,
            )
        )
    links = dict()
    if len(ret) >= size:
        links["next"] = str(
            request.url_for(
                "get_team_topic_docs", team_topic_name=team_topic_name
            ).include_query_params(type=type, page=page + 1, size=size)
        )
    if page > 0:
        links["prev"] = str(
            request.url_for(
                "get_team_topic_docs", team_topic_name=team_topic_name
            ).include_query_params(type=type, page=page - 1, size=size)
        )
    return dict(
        result=ret,
        links=links,
    )
