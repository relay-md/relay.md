# -*- coding: utf-8 -*-

import hashlib
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
    body = await request.body()

    # Checksum
    hashing_obj = hashlib.sha256()
    hashing_obj.update(body)
    sha256 = hashing_obj.hexdigest()

    asset_repo = AssetRepo(db)
    asset = asset_repo.get_by_kwargs(
        document_id=document.id,
        filename=filename,
    )
    if not asset:
        asset = asset_repo.create_from_kwargs(
            user_id=user.id,
            document_id=document.id,
            filename=filename,
            filesize=len(body),
            checksum_sha256=sha256,
        )
        asset_content_repo = AssetContentRepo()
        asset_content_repo.create(asset.id, body)
    else:
        if asset.checksum_sha256 != sha256:
            # file has changed, updated it
            asset_content_repo = AssetContentRepo()
            asset_content_repo.create(asset.id, body)
            asset = asset_repo.update(asset, filesize=len(body), checksum_sha256=sha256)
    return dict(result=dict(id=asset.id))
