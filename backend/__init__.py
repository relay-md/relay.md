# -*- coding: utf-8 -*-
from authlib.integrations.starlette_client import OAuth

from . import config

__version__ = "0.1.2"

oauth = OAuth()
oauth.register(
    name="github",
    client_id=config.config.GITHUB_CLIENT_ID,
    client_secret=config.config.GITHUB_CLIENT_SECRET,
    client_kwargs={"scope": "read:user"},
    access_token_url="https://github.com/login/oauth/access_token",
    authorize_url="https://github.com/login/oauth/authorize",
    api_base_url="https://api.github.com/",
)
