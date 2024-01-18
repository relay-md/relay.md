# -*- coding: utf-8 -*-
from ..config import get_config
from .minio import MinioAbstractRepo


class DocumentBodyRepo(MinioAbstractRepo):
    BUCKET = get_config().MINIO_BUCKET

    def get_file_name(self, id, postfix=None):
        name = str(id)
        # We are nesting uuid based filenames into 4 sub directories
        return f"{name[0]}/{name[1]}/{name[2]}/{name[3]}/{name}.md"
