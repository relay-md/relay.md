# -*- coding: utf-8 -*-
import abc
import io
from typing import List, Optional, Union
from uuid import UUID

from minio import Minio
from minio.commonconfig import CopySource

from ..config import get_config


class MinioAbstractRepo:
    BUCKET = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._client = Minio(
            get_config().MINIO_ENDPOINT,
            access_key=get_config().MINIO_ACCESS_KEY,
            secret_key=get_config().MINIO_SECRET_KEY,
            secure=get_config().MINIO_SECURE,
        )

    def create(
        self, id: UUID, data: Union[bytes, str], filename: Optional[str] = None
    ) -> None:
        if not self._client.bucket_exists(self.BUCKET):
            self._client.make_bucket(self.BUCKET)
        if isinstance(data, str):
            data = bytes(data, "utf-8")
        if filename:
            file_postfix = filename.split(".")[-1]
        else:
            file_postfix = ""
        # FIXME: we need to deal with mime type here!
        self._client.put_object(
            self.BUCKET,
            self.get_file_name(id, file_postfix),
            io.BytesIO(data),
            len(data),
            content_type="text/markdown",
        )

    @abc.abstractmethod
    def get_file_name(self, id, postfix=None):
        raise NotImplementedError()

    def get_by_id(self, id: UUID) -> bytes:
        response = None
        try:
            response = self._client.get_object(self.BUCKET, self.get_file_name(id))
            return response.data
        finally:
            if response:
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

    def delete(self, id: UUID) -> None:
        self._client.remove_object(self.BUCKET, self.get_file_name(id))
