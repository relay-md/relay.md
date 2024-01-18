# -*- coding: utf-8 -*-
import enum
from typing import Generic, List, Optional, TypeVar, Union
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

DataT = TypeVar("DataT", bound=BaseModel)


class DocumentShareType(enum.IntFlag):
    PUBLIC = 2**0
    SHARED_WITH_USER = 2**1
    SUBSCRIBED_TEAM = 2**2


class Error(BaseModel):
    """Error responses"""

    code: Optional[int] = None
    type: Optional[str] = None
    detail: Optional[dict] = None
    message: str


class Response(BaseModel, Generic[DataT]):
    """General Response for result and error"""

    result: Optional[DataT] = None
    error: Optional[Error] = None


class TeamResponse(BaseModel):
    id: UUID
    model_config = ConfigDict(from_attributes=True)


class TopicResponse(BaseModel):
    id: UUID
    model_config = ConfigDict(from_attributes=True)


class DocumentFrontMatter(BaseModel):
    relay_document: Optional[UUID] = Field(None, alias="relay-document")
    relay_to: Union[str, List[str]] = Field(alias="relay-to")
    relay_filename: Optional[str] = Field(None, alias="relay-filename")
    relay_title: Optional[str] = Field(None, alias="relay-title")
    model_config = ConfigDict(
        from_attributes=True, extra="allow", populate_by_name=True
    )

    @field_validator("relay_to")
    @classmethod
    def ensure_list(cls, value: Union[str, List[str]]):
        if not isinstance(value, list):
            return [value]

        return value


class DocumentResponse(DocumentFrontMatter):
    body: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)


class DocumentIdentifierResponse(BaseModel):
    """This schema is only used when listing all documents that need to be
    fetched individually"""

    relay_document: Optional[UUID] = Field(None, alias="relay-document")
    relay_to: Union[str, List[str]] = Field(alias="relay-to")
    relay_filename: Optional[str] = Field(None, alias="relay-filename")
    model_config = ConfigDict(from_attributes=True, populate_by_name=True)


class VersionResponse(BaseModel):
    version: str


class AssetReponse(BaseModel):
    id: UUID
