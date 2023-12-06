# -*- coding: utf-8 -*-
import io
from typing import List
from uuid import UUID

from minio import Minio

from ..config import config
from .base import AbstractRepository


class MinioAbstractRepo(AbstractRepository):
    # TODO: access to s3 documents
    # filename == document id
    # nested folder structure with 6 nested nibbles
    # maybe take a look at how sccache does it
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = Minio(
            config.MINIO_ENDPOINT,
            access_key=config.MINIO_ACCESS_KEY,
            secret_key=config.MINIO_SECRET_KEY,
            secure=config.MINIO_SECURE,
        )

    def create(self, id: UUID, data: bytes | str) -> None:
        if not self._client.bucket_exists(self.BUCKET):
            self._client.make_bucket(self.BUCKET)
        if isinstance(data, str):
            data = bytes(data, "utf-8")
        # Upload data with content-type.
        self._client.put_object(
            self.BUCKET,
            self.get_file_name(id),  # TODO: want to split this into dirs
            io.BytesIO(data),
            len(data),
            content_type="text/markdown",
        )

    def get_file_name(self, id):
        return f"{str(id)}.md"

    def get_by_id(self, id: UUID) -> bytes:
        try:
            response = self._client.get_object(self.BUCKET, self.get_file_name(id))
            return response.data.decode("utf-8")
        finally:
            try:
                response.close()
                response.release_conn()
            except Exception:
                pass

    def list(self, key: str, **kwargs) -> List[UUID]:
        raise NotImplementedError

    def update(self, id: UUID, data: bytes) -> None:
        self.create(id, data)


class DocumentBodyRepo(MinioAbstractRepo):
    BUCKET = "documents"
