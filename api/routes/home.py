import json
from fastapi import APIRouter, Depends, HTTPException, Request, Response
from starlette.responses import HTMLResponse, RedirectResponse
from .. import oauth

router = APIRouter(prefix="")

@router.get('/')
async def homepage(request: Request):
    user = request.session.get('user')
    user_id = request.session.get('user_id')
    access_token = request.session.get('access_token')
    if user:
        data = json.dumps(user, indent=4)
        html = (
            f'<pre>{data}</pre>'
            f'<pre>{user_id}</pre>'
            f'<pre>{access_token}</pre>'
            '<a href="/logout">logout</a>'
        )
        return HTMLResponse(html)
    return HTMLResponse('<a href="/login/github">login</a>')
