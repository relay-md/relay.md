# -*- coding: utf-8 -*-
from typing import Generic, List, Optional, TypeVar
from uuid import UUID

from pydantic import BaseModel, Extra, Field
from pydantic.generics import GenericModel

DataT = TypeVar("DataT")


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


class TeamTopicReponse(BaseModel):
    # id: UUID
    name: str

    class Config:
        orm_mode = True


class DocumentFrontMatter(BaseModel):
    relay_document: Optional[UUID] = Field(alias="relay-document")
    relay_to: List[str] = Field(alias="relay-to")
    relay_filename: Optional[str] = Field(alias="relay-filename")

    class Config:
        orm_mode = True
        extra = Extra.allow
        allow_population_by_field_name = True


class DocumentResponse(DocumentFrontMatter):
    body: Optional[str]

    class Config:
        orm_mode = True


class DocumentIdentifierResponse(BaseModel):
    id: UUID
    filename: str
    to: List[TeamTopicReponse]

    class Config:
        orm_mode = True
