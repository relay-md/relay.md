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
    name: str = Field()

    class Config:
        orm_mode = True


class DocumentResponse(BaseModel):
    id: UUID
    filename: str
    to: List[TeamTopicReponse] = Field(alias="team_topics")
    # FIXME: should we maybe deal with bytes instead of strings?
    body: Optional[str]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class DocumentFrontMatter(BaseModel):
    relay_to: List[str]
    rid: Optional[UUID]
    relay_filename: Optional[str]

    class Config:
        orm_mode = True
        extra = Extra.allow


class DocumentIdentifierResponse(BaseModel):
    id: UUID
    filename: str
    to: List[TeamTopicReponse]

    class Config:
        orm_mode = True
