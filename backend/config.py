# -*- coding: utf-8 -*-
""" Configuration classes

Allow to load values from environment variables.
"""
from typing import List, Optional
from uuid import UUID

from pydantic_settings import BaseSettings, SettingsConfigDict


class SQLAlchemyEngineOptions(BaseSettings):
    # list of all options: https://docs.sqlalchemy.org/en/13/core/engines.html#engine-creation-api
    pool_pre_ping: bool = True  # helps reconnect in case a SQL server goes down
    pool_recycle: int = 300  # this setting causes the pool to recycle connections after the given number of seconds
    pool_size: Optional[int] = 32
    max_overflow: Optional[int] = 64


class Settings(BaseSettings):
    """General Settings"""

    SECRET_KEY: str = "asfafgrzlihdgssdgn"

    # SQL Settings
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///default.db"
    SQLALCHEMY_ENGINE_OPTIONS: Optional[SQLAlchemyEngineOptions] = None
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False

    # Limit API access by means of CORS
    API_ALLOWED_ORIGINS: List[str] = ["*"]

    # Email
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_PORT: int = 587
    MAIL_SERVER: str = "smtp.mailgun.org"
    MAIL_STARTTLS: bool = True
    MAIL_SSL_TLS: bool = False
    # MAIL_DEBUG: bool = False
    MAIL_FROM: str = "noreply@example.com"

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

    # Checkout.com
    CHECKOUTCOM_CLIENT_ID: str
    CHECKOUTCOM_CLIENT_SECRET: str
    CHECKOUTCOM_DESCRIPTION: str = "Payment for Relay.md"
    CHECKOUTCOM_CHANNEL_ID: str

    # Early access configs
    ENABLE_EARLY_ACCESS: bool = True
    NEW_USER_SUBSCRIBE_TO: List[str] = ["news@relay.md"]

    RELAY_NEWS_TEAM_TOPIC_ID: Optional[UUID] = None

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


config = None


def get_config():
    global config
    if config is None:
        config = Settings()
    return config
