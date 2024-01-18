# -*- coding: utf-8 -*-

from typing import Optional

from fastapi import Depends, Request

from ...database import Session, get_session
from ...exceptions import BadRequest
from ...models.document import Document
from ...models.user import User
from ...repos.asset import AssetContentRepo, AssetRepo
from ...schema import AssetReponse, Response
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
    asset_repo = AssetRepo(db)
    asset = asset_repo.create_from_kwargs(
        user_id=user.id,
        document_id=document.id,
        filename=filename,
    )
    asset_content_repo = AssetContentRepo()
    asset_content_repo.create(asset.id, await request.body())
    # FIXME:
    # TODO:
    #  * Check that file already exists and update the existing file instead of
    #  creating a new one
    #  * implement an api that lets you check if the asset was uploaded already
    #  * use sha256 hashes to check against online version of the file (also in
    #  the plugin)
    return dict(result=dict(id=asset.id))
