# -*- coding: utf-8 -*-
""" Configuration classes

Allow to load values from environment variables.
"""
from typing import List, Optional, Tuple
from uuid import UUID

from pydantic_settings import BaseSettings, SettingsConfigDict


class SQLAlchemyEngineOptions(BaseSettings):
    # list of all options: https://docs.sqlalchemy.org/en/13/core/engines.html#engine-creation-api
    pool_pre_ping: bool = True  # helps reconnect in case a SQL server goes down
    # this setting causes the pool to recycle connections after the given number of seconds
    pool_recycle: int = 300
    pool_size: Optional[int] = 32
    max_overflow: Optional[int] = 64


class Settings(BaseSettings):
    """General Settings"""

    SECRET_KEY: str = "asfafgrzlihdgssdgn"

    # SQL Settings
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///default.db"
    SQLALCHEMY_ENGINE_OPTIONS: Optional[
        SQLAlchemyEngineOptions
    ] = SQLAlchemyEngineOptions()
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False

    # Admins
    ADMIN_USER_IDS: List[str] = []

    # Limit API access by means of CORS
    API_ALLOWED_ORIGINS: List[str] = ["*"]

    # Email
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "mail.chainsquad.com"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    # MAIL_DEBUG: bool = False
    MAIL_FROM: str = "noreply@relay.md"
    MAIL_ADMIN: str = "fabian@relay.md"

    # Oauth Client data
    GITHUB_CLIENT_ID: Optional[str]
    GITHUB_CLIENT_SECRET: Optional[str]
    GOOGLE_CLIENT_ID: Optional[str]
    GOOGLE_CLIENT_SECRET: Optional[str]

    # Mailchimp
    MAILCHIMP_API_SERVER: Optional[str]
    MAILCHIMP_API_KEY: Optional[str]
    MAILCHIMP_LIST_ID: Optional[str]

    # Minio access
    MINIO_ENDPOINT: str = "play.min.io"
    MINIO_ACCESS_KEY: Optional[str]
    MINIO_SECRET_KEY: Optional[str]
    MINIO_SECURE: bool = True
    MINIO_BUCKET: str = "documents"

    PAYMENT_BASIC_AUTH_WHITELIST: List[Tuple[str, str]] = [("foo", "bar")]

    STRIPE_API_KEY: Optional[str] = ""
    STRIPE_API_PRIVATE_KEY: Optional[str] = ""
    STRIPE_WEBHOOK_SECRET: Optional[str] = ""
    STRIPE_RETURN_URL_SUCCESS: str = "https://relay.md/payment/success"
    STRIPE_RETURN_URL_CANCEL: str = "https://relay.md/payment/failed"
    STRIPE_CUSTOMER_PORTAL_URL: Optional[str] = ""

    PRICING_TEAM_YEARLY: float = 30.0
    PRICING_TEAM_MONTHLY: float = 3.0

    NEW_USER_SUBSCRIBE_TO: List[str] = ["news@relay.md"]
    RELAY_NEWS_TEAM_TOPIC_ID: Optional[UUID] = None

    FASTAPI_CONFIG: dict = {
        "title": "Relay.md Developer Access",
        "description": "Access relay.md features through API",
        "contact": {
            "name": "Fabian Schuh",
            "email": "fabian@relay.md",
        },
        "openapi_tags": [
            {"name": "v1", "description": "Version 1 Implementation of the API"},
            {"name": "default", "description": "Internal use"},
        ],
    }

    SENTRY_DSN: Optional[str] = ""

    PRERENDER_USER_AGENTS: List[str] = [
        "googlebot",
        "bingbot",
        "yandex",
        "baiduspider",
        "twitterbot",
        "facebookexternalhit",
        "rogerbot",
        "linkedinbot",
        "embedly",
        "quora link preview",
        "showyoubot",
        "outbrain",
        "pinterest",
        "slackbot",
        "vkShare",
        "W3C_Validator",
    ]
    PRERENDER_REDIRECT: str = "https://prerender.infra.chainsquad.com/"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = None


def get_config():
    global config
    if config is None:
        config = Settings()
    return config
