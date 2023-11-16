# -*- coding: utf-8 -*-
import io
from typing import List
from uuid import UUID

from minio import Minio

from . import AbstractRepository


class MinioAbstracRepo(AbstractRepository):
    # TODO: access to s3 documents
    # filename == document id
    # nested folder structure with 6 nested nibbles
    # maybe take a look at how sccache does it
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # FIXME: own minio deployment here
        # make use of env credentials
        self._client = Minio("play.min.io")

    def create(self, id: UUID, data: bytes) -> None:
        # Upload data with content-type.
        self._client.put_object(
            self.BUCKET,
            str(id),  # TODO: want to split this into dirs
            io.BytesIO(data),
            len(data),
            content_type="text/markdown",
        )

    def get_by_id(self, id: UUID) -> bytes:
        raise NotImplementedError

    def list(self, key: str, **kwargs) -> List[UUID]:
        raise NotImplementedError

    def update(self, id: UUID, item: bytes) -> None:
        raise NotImplementedError


class DocumentBodyRepo(MinioAbstracRepo):
    BUCKET = "documents"
