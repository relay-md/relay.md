# -*- coding: utf-8 -*-
from typing import Optional, Union
from uuid import UUID

from ..config import get_config
from ..models.asset import Asset
from .base import DatabaseAbstractRepository
from .minio import MinioAbstractRepo


class AssetRepo(DatabaseAbstractRepository):
    ORM_Model = Asset


class AssetContentRepo(MinioAbstractRepo):
    BUCKET = get_config().MINIO_BUCKET_ASSETS

    def create(
        self,
        id: UUID,
        data: Union[bytes, str],
        filename: Optional[str] = None,
        content_type: Optional[str] = "application/octet-stream",
    ) -> None:
        super().create(id, data, filename=filename, content_type=content_type)

    def get_file_name(self, id, postfix: Optional[str] = ""):
        name = str(id)
        # We are nesting uuid based filenames into 4 sub directories
        ret = f"{name[0]}/{name[1]}/{name[2]}/{name[3]}/{name}"
        if postfix:
            ret += f".{postfix}"
        return ret
