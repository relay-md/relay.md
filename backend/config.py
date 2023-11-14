# -*- coding: utf-8 -*-
""" Configuration classes

Allow to load values from environment variables.
"""
from typing import List, Optional

from pydantic import BaseSettings


class SQLAlchemyEngineOptions(BaseSettings):
    # list of all options: https://docs.sqlalchemy.org/en/13/core/engines.html#engine-creation-api
    pool_pre_ping: bool = True  # helps reconnect in case a SQL server goes down
    pool_recycle: int = 300  # this setting causes the pool to recycle connections after the given number of seconds
    pool_size: Optional[int] = 32
    max_overflow: Optional[int] = 64


class CelerySettings(BaseSettings):
    """Celery Configurations

    Allows to specify the BROKER_URL and RESULT_BACKEND
    """

    broker_url: str = "redis://localhost:6379"

    # Result backend to go to a sql database
    # for a mysql database use 'db+mysql://scott:tiger@localhost/foo' or "db+sqlite:///results.db"
    # more documentation here:
    # https://docs.celeryq.dev/en/stable/userguide/configuration.html#conf-database-result-backend
    result_backend: str = "redis://localhost:6379"

    # Enables extended task result attributes (name, args, kwargs, worker,
    # retries, queue, delivery_info) to be written to backend.
    result_extended: bool = True

    # Database storage engine configs
    database_engine_options: dict = dict()
    database_table_names: dict = dict(task="celery_task", group="celery_group")

    beat_schedule: dict = {}

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


class Settings(BaseSettings):
    """General Settings"""

    SECRET_KEY: str = "asfafgrzlihdgssdgn"

    # SQL Settings
    SQLALCHEMY_DATABASE_URI: str = "sqlite:///default.db"
    SQLALCHEMY_ENGINE_OPTIONS: SQLAlchemyEngineOptions = SQLAlchemyEngineOptions()
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    SQLALCHEMY_ECHO: bool = False

    # Celery settings
    CELERY_CONF: CelerySettings = CelerySettings()

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
    GITHUB_CLIENT_ID: str
    GITHUB_CLIENT_SECRET: str

    # Mailchimp
    MAILCHIMP_API_SERVER: str
    MAILCHIMP_API_KEY: str
    MAILCHIMP_LIST_ID: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


config = Settings()
