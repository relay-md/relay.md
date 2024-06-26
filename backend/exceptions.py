# -*- coding: utf-8 -*-
""" Exception handling hook. This is called from api.py
    https://github.com/tiangolo/fastapi/issues/1667
"""

import urllib

from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from starlette.responses import RedirectResponse

from .repos.user import User
from .templates import templates
from .utils.user import get_optional_user


class BaseAPIException(Exception):
    """Our base exceptions we use for custom exceptions on the API"""

    code: int


class NotAllowed(BaseAPIException):
    """User with this name already exists in db"""

    code = status.HTTP_403_FORBIDDEN


class DatabaseException(BaseAPIException):
    """Bad user request"""

    code = status.HTTP_400_BAD_REQUEST


class BadRequest(BaseAPIException):
    """Bad user request"""

    code = status.HTTP_400_BAD_REQUEST


class NotFound(BaseAPIException):
    """404"""

    code = status.HTTP_404_NOT_FOUND


class Unauthorized(BaseAPIException):
    """401"""

    code = status.HTTP_401_UNAUTHORIZED


class AlreadySubscribed(Exception):
    pass


class LoginRequiredException(BaseAPIException):
    """401"""

    code = status.HTTP_401_UNAUTHORIZED
    next_url = None

    def __init__(self, *args, next_url=None, **kwargs):
        super().__init__(*args, *kwargs)
        self.next_url = next_url


class WebhookException(BaseAPIException):
    code = status.HTTP_400_BAD_REQUEST


async def handle_exception(request: Request, exc: BaseAPIException):
    """Our internal exceptions are handled here"""
    from .schema import Response

    error = dict(message=str(exc), code=exc.code)
    content: Response = Response(error=error)
    return JSONResponse(content=content.model_dump(exclude_none=True), status_code=200)


async def handle_http_exception(request: Request, exc: HTTPException):
    from .schema import Response

    error = dict(message=str(exc.detail))
    content: Response = Response(error=error)
    return JSONResponse(content=content.model_dump(exclude_none=True), status_code=200)


async def handle_basegateway_exception(request: Request, exc: HTTPException):
    from .schema import Response

    error = dict(message=str(exc))
    content: Response = Response(error=error)
    return JSONResponse(content=content.model_dump(exclude_none=True), status_code=200)


async def unhandled_exception(request: Request, exc: Exception):
    from .schema import Response

    error = dict(message="unhandled exception", detail=dict(message=str(exc)))
    content: Response = Response(error=error)
    return JSONResponse(content=content.model_dump(exclude_none=True), status_code=200)


async def web_handle_exception(
    request: Request,
    exc: Exception,
    user: User = Depends(get_optional_user),
):
    # required for top
    return templates.TemplateResponse("exception.pug", context=dict(**locals()))


async def web_unhandled_exception(
    request: Request,
    exc: Exception,
    user: User = Depends(get_optional_user),
):
    return templates.TemplateResponse("exception.pug", context=dict(**locals()))


async def web_handle_webhookexception(
    request: Request,
    exc: Exception,
    user: User = Depends(get_optional_user),
):
    from .schema import Response

    error = dict(message=str(exc), detail={})
    content: Response = Response(error=error)
    return JSONResponse(content=content.model_dump(exclude_none=True), status_code=400)


async def redirect_to_login(
    request: Request,
    exc: LoginRequiredException,
    user: User = Depends(get_optional_user),
):
    url = str(request.url_for("login"))
    if exc.next_url:
        parsed = list(urllib.parse.urlparse(url))
        parsed[4] = urllib.parse.urlencode(dict(next=str(exc.next_url)))
        url = urllib.parse.urlunparse(parsed)
    return RedirectResponse(url=url)


def include_app(app):
    app.add_exception_handler(BaseAPIException, handle_exception)
    app.add_exception_handler(HTTPException, handle_http_exception)
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
    app.add_exception_handler(Exception, unhandled_exception)


def include_app_web(app):
    app.add_exception_handler(LoginRequiredException, redirect_to_login)
    app.add_exception_handler(NotAllowed, web_handle_exception)
    app.add_exception_handler(NotFound, web_handle_exception)
    app.add_exception_handler(Unauthorized, web_handle_exception)
    app.add_exception_handler(WebhookException, web_handle_webhookexception)
    app.add_exception_handler(Exception, web_unhandled_exception)
