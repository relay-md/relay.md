# -*- coding: utf-8 -*-
from ..config import get_config
from ..models.asset import Asset
from .base import DatabaseAbstractRepository
from .minio import MinioAbstractRepo


class AssetRepo(DatabaseAbstractRepository):
    ORM_Model = Asset


class AssetContentRepo(MinioAbstractRepo):
    BUCKET = get_config().MINIO_BUCKET_ASSETS

    def get_file_name(self, id, postfix=""):
        name = str(id)
        # We are nesting uuid based filenames into 4 sub directories
        ret = f"{name[0]}/{name[1]}/{name[2]}/{name[3]}/{name}"
        if postfix:
            ret += f".{postfix}"
        return ret
