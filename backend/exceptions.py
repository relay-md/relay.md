# -*- coding: utf-8 -*-
""" Exception handling hook. This is called from api.py
    https://github.com/tiangolo/fastapi/issues/1667
"""


from fastapi import Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse

from .repos.user import User
from .templates import templates
from .utils.user import get_optional_user


class BaseAPIException(Exception):
    """Our base exceptions we use for custom exceptions on the API"""

    code: int
    status_code: int


class NotAllowed(BaseAPIException):
    """User with this name already exists in db"""

    code = 10000
    status_code = status.HTTP_403_FORBIDDEN


class BadRequest(BaseAPIException):
    """Bad user request"""

    code = 10001
    status_code = status.HTTP_400_BAD_REQUEST


class NotFound(BaseAPIException):
    """404"""

    code = 10002
    status_code = status.HTTP_404_NOT_FOUND


class Unauthorized(BaseAPIException):
    """401"""

    code = 10003
    status_code = status.HTTP_401_UNAUTHORIZED


async def handle_exception(request: Request, exc: BaseAPIException):
    """Our internal exceptions are handled here"""
    from .schema import Response

    error = dict(message=str(exc), status_code=exc.status_code, code=exc.code)
    content: Response = Response(error=error)
    return JSONResponse(
        content=content.dict(exclude_none=True), status_code=exc.status_code
    )


async def handle_http_exception(request: Request, exc: HTTPException):
    from .schema import Response

    error = dict(message=str(exc.detail))
    status_code = exc.status_code
    content: Response = Response(error=error)
    return JSONResponse(
        content=content.dict(exclude_none=True), status_code=status_code
    )


async def handle_basegateway_exception(request: Request, exc: HTTPException):
    from .schema import Response

    error = dict(message=str(exc))
    status_code = 400
    content: Response = Response(error=error)
    return JSONResponse(
        content=content.dict(exclude_none=True), status_code=status_code
    )


async def unhandled_exception(request: Request, exc: Exception):
    from .schema import Response

    error = dict(message="unhandled exception", detail=dict(message=str(exc)))
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    content: Response = Response(error=error)
    return JSONResponse(
        content=content.dict(exclude_none=True), status_code=status_code
    )


async def web_handle_exception(
    request: Request, exc: Exception, user: User = Depends(get_optional_user)
):
    # required for top
    user = None
    return templates.TemplateResponse("exception.html", context=dict(**locals()))


def include_app(app):
    app.add_exception_handler(BaseAPIException, handle_exception)
    app.add_exception_handler(HTTPException, handle_http_exception)
    app.add_exception_handler(Exception, unhandled_exception)


def include_app_web(app):
    # FIXME: need to deal with making nicer
    app.add_exception_handler(Exception, web_handle_exception)
