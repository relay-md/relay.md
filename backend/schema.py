# -*- coding: utf-8 -*-
import enum
from typing import Generic, List, Optional, TypeVar, Union
from uuid import UUID

from pydantic import BaseModel, Extra, Field, validator
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


class DocumentShareType(enum.IntFlag):
    PUBLIC = 2**0
    SHARED_WITH_USER = 2**1
    SUBSCRIBED_TEAM = 2**2


class Error(BaseModel):
    """Error responses"""

    code: Optional[int]
    type: Optional[str]
    detail: Optional[dict]
    message: str


class Response(GenericModel, Generic[DataT]):
    """General Response for result and error"""

    result: Optional[DataT]
    error: Optional[Error]


class TeamResponse(BaseModel):
    id: UUID

    class Config:
        orm_mode = True


class TopicResponse(BaseModel):
    id: UUID

    class Config:
        orm_mode = True


class DocumentFrontMatter(BaseModel):
    relay_document: Optional[UUID] = Field(alias="relay-document")
    relay_to: Union[str, List[str]] = Field(alias="relay-to")
    relay_filename: Optional[str] = Field(alias="relay-filename")
    relay_title: Optional[str] = Field(alias="relay-title")

    class Config:
        orm_mode = True
        extra = Extra.allow
        allow_population_by_field_name = True

    @validator("relay_to")
    def ensure_list(cls, value: Union[str, List[str]]):
        if not isinstance(value, list):
            return [value]

        return value


class DocumentResponse(DocumentFrontMatter):
    body: Optional[str]

    class Config:
        orm_mode = True


class DocumentIdentifierResponse(BaseModel):
    """This schema is only used when listing all documents that need to be
    fetched individually"""

    relay_document: Optional[UUID] = Field(alias="relay-document")
    relay_to: Union[str, List[str]] = Field(alias="relay-to")
    relay_filename: Optional[str] = Field(alias="relay-filename")

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class VersionResponse(BaseModel):
    version: str
