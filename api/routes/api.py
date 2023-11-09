# -*- coding: utf-8 -*-
from uuid import UUID

from fastapi import APIRouter, Request

router = APIRouter(prefix="/api")


@router.post("/doc")
async def post_doc(request: Request):
    body = await request.body()
    body = body.decode("utf-8")
    return body


@router.get("/doc/{uid}")
async def get_doc(request: Request, uid: UUID):
    return ""


@router.put("/doc/{uid}")
async def put_doc(request: Request, uid: UUID):
    return ""
