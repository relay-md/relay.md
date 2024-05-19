# -*- coding: utf-8 -*-

import hashlib
from datetime import datetime
from typing import Optional
from uuid import UUID

from fastapi import Depends, Request
from fastapi.responses import StreamingResponse

from ...database import Session, get_session
from ...exceptions import BadRequest, NotAllowed, NotFound
from ...models.document import Document
from ...models.user import User
from ...repos.asset import AssetContentRepo, AssetRepo
from ...repos.team import TeamRepo
from ...repos.user import UserRepo
from ...schema import AssetReponse, Response, SuccessResponse
from . import get_document, require_authenticated_user, router


@router.post(
    "/assets/{id}",
    tags=["v1"],
    response_model=Response[AssetReponse],
    response_model_exclude_unset=True,
    response_model_by_alias=True,
)
async def post_asset(
    request: Request,
    filename: Optional[str] = "",
    document: Document = Depends(get_document),
    user: User = Depends(require_authenticated_user),
    db: Session = Depends(get_session),
):
    """The id references the document id so the asset is linked to the document
    that uses it!"""
    content_type = request.headers.get("content-type", "application/octet-stream")
    if content_type != "application/octet-stream":
        raise BadRequest("Unsupported content-type! Requires application/octet-stream")
    # Get filename from header
    if not filename:
        filename = request.headers.get("x-relay-filename")
    if not filename:
        raise BadRequest(
            "Filename query string, or x-relay-filename header not pressent"
        )
    body = await request.body()

    # Checksum
    hashing_obj = hashlib.sha256()
    hashing_obj.update(body)
    sha256 = hashing_obj.hexdigest()

    asset_repo = AssetRepo(db)
    asset = asset_repo.get_by_kwargs(
        document_id=document.id,
        filename=filename,
        deleted_at=None,
    )
    if asset:
        raise BadRequest(
            "An asset witht hat filename is already tied to the document. Please use PUT instead to update the asset"
        )

    # add size to teams
    TeamRepo(db)

    asset = asset_repo.create_from_kwargs(
        user_id=user.id,
        document_id=document.id,
        filename=filename,
        filesize=len(body),
        checksum_sha256=sha256,
    )
    asset_content_repo = AssetContentRepo()
    asset_content_repo.create(asset.id, body)

    return dict(result=AssetReponse.from_orm(asset))


@router.put(
    "/assets/{id}",
    tags=["v1"],
    response_model=Response[AssetReponse],
    response_model_exclude_unset=True,
    response_model_by_alias=True,
)
async def put_asset(
    request: Request,
    id: UUID,
    user: User = Depends(require_authenticated_user),
    db: Session = Depends(get_session),
):
    content_type = request.headers.get("content-type", "application/octet-stream")
    if content_type != "application/octet-stream":
        raise BadRequest("Unsupported content-type! Requires application/octet-stream")
    body = await request.body()

    # Checksum
    hashing_obj = hashlib.sha256()
    hashing_obj.update(body)
    sha256 = hashing_obj.hexdigest()

    asset_repo = AssetRepo(db)
    asset = asset_repo.get_by_kwargs(
        id=id,
        deleted_at=None,
    )
    if not asset:
        raise NotFound("Asset not found")
    if asset.checksum_sha256 != sha256:
        len(body) - asset.filesize

        # FIXME: this gets messy if team_topics get fewer
        TeamRepo(db)

        # file has changed, updated it
        asset_content_repo = AssetContentRepo()
        asset_content_repo.create(asset.id, body)
        asset = asset_repo.update(
            asset,
            filesize=len(body),
            checksum_sha256=sha256,
            last_updated_at=datetime.utcnow(),
        )

    return dict(result=AssetReponse.from_orm(asset))


@router.get("/assets/{id}", tags=["v1"])
async def get_asset(
    id: UUID,
    request: Request,
    user: User = Depends(require_authenticated_user),
    db: Session = Depends(get_session),
):
    asset_repo = AssetRepo(db)
    asset = asset_repo.get_by_kwargs(id=id)
    if not asset or asset.deleted_at:
        raise NotFound("Asset not found")
    if asset.user_id != user.id:
        user_repo = UserRepo(db)
        # TODO: find a more efficient way to query all team topics in document
        for team_topic in asset.document.team_topics:
            if user_repo.has_subscribed_to_topic_in_team(user, team_topic):
                break
        raise NotAllowed("Not your asset")
    content_type = request.headers.get("content-type")
    if content_type == "application/json":
        return AssetReponse.from_orm(asset)
    else:
        asset_content_repo = AssetContentRepo()
        data = asset_content_repo.get_by_id(id)

        # https://stackoverflow.com/questions/55873174/how-do-i-return-an-image-in-fastapi
        def yield_data():
            yield data

        return StreamingResponse(
            content=yield_data(), media_type="application/octet-stream"
        )


@router.delete(
    "/assets/{id}",
    tags=["v1"],
    response_model=Response[SuccessResponse],
)
async def delete_asset(
    id: UUID,
    user: User = Depends(require_authenticated_user),
    db: Session = Depends(get_session),
):
    asset_repo = AssetRepo(db)
    asset = asset_repo.get_by_kwargs(id=id)
    if not asset:
        raise NotFound("Asset not found")
    if asset.user_id != user.id:
        raise NotAllowed("Not your asset")
    asset_repo.update(asset, deleted_at=datetime.utcnow())

    # remove size from teams
    TeamRepo(db)

    return dict(result=dict(success=True))
