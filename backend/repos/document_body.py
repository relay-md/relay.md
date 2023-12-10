# -*- coding: utf-8 -*-
import io
from typing import List, Union
from uuid import UUID

from minio import Minio
from minio.commonconfig import CopySource

from ..config import get_config
from .base import AbstractRepository


class MinioAbstractRepo(AbstractRepository):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = Minio(
            get_config().MINIO_ENDPOINT,
            access_key=get_config().MINIO_ACCESS_KEY,
            secret_key=get_config().MINIO_SECRET_KEY,
            secure=get_config().MINIO_SECURE,
        )

    def create(self, id: UUID, data: Union[bytes, str]) -> None:
        if not self._client.bucket_exists(self.BUCKET):
            self._client.make_bucket(self.BUCKET)
        if isinstance(data, str):
            data = bytes(data, "utf-8")
        # Upload data with content-type.
        self._client.put_object(
            self.BUCKET,
            self.get_file_name(id),
            io.BytesIO(data),
            len(data),
            content_type="text/markdown",
        )

    def get_file_name(self, id):
        name = str(id)
        # We are nesting uuid based filenames into 4 sub directories
        return f"{name[0]}/{name[1]}/{name[2]}/{name[3]}/{name}.md"

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

    def list(self, prefix="", recursive=False) -> List[UUID]:
        return self._client.list_objects(self.BUCKET, prefix, recursive=recursive)

    def copy(self, source, destination):
        return self._client.copy_object(
            self.BUCKET, destination, CopySource(self.BUCKET, source)
        )

    def stat(self, path: str):
        return self._client.stat_object(self.BUCKET, path)

    def update(self, id: UUID, data: bytes) -> None:
        self.create(id, data)


class DocumentBodyRepo(MinioAbstractRepo):
    BUCKET = "documents"
