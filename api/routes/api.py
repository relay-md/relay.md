import json
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from starlette.responses import HTMLResponse, RedirectResponse
from .. import oauth

router = APIRouter(prefix="/api")

@router.post('/doc')
async def doc(request: Request):
    body = await request.body()
    body = body.decode("utf-8")
    return body


@router.get('/doc/{uid}')
async def doc(request: Request, uid: UUID):
    return ""


@router.put('/doc/{uid}')
async def doc(request: Request, uid: UUID):
    return ""
