# -*- coding: utf-8 -*-
from sqlalchemy import select
from ..models.document import Document
from ..models.team_topic import TeamTopic
from ..models.user import User
from ..models.team import Team
from ..models.topic import Topic
from . import DatabaseAbstractRepository


class DocumentRepo(DatabaseAbstractRepository):
    ORM_Model = Document

    def _update_user_latest_document(self, user: User, document: Document):
        user.latest_document_datetime = document.last_updated_at
        self._db.commit()

    def get_recent_documents_for_me(self, user:User, page: int = 0, size: int = 10):
        ret = list(self._db.scalars(
            select(Document)
            # TODO: add extra joins and filters as soon as we have private repos
            .filter(Document.last_updated_at > user.latest_document_datetime)
            .order_by(Document.last_updated_at.asc())
            .offset(page*size)
            .limit(size)
        ))
        if ret:
            self._update_user_latest_document(user, ret[-1])
        return ret

    def get_my_documents(self, user: User, page: int = 0, size: int = 10):
        return self._db.scalars(
            select(Document)
            .filter(Document.user_id == user.id)
            .order_by(Document.last_updated_at.desc())
            .offset(page*size)
            .limit(size)
        )
