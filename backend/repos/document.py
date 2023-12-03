# -*- coding: utf-8 -*-
from sqlalchemy import select

from ..models.access_token import AccessToken
from ..models.document import Document
from ..models.document_team_topic import DocumentTeamTopic
from ..models.document_user import DocumentUser
from ..models.team_topic import TeamTopic
from ..models.user import User
from ..schema import DocumentShareType
from .base import DatabaseAbstractRepository


class DocumentRepo(DatabaseAbstractRepository):
    ORM_Model = Document

    def _update_user_latest_document(
        self, access_token: AccessToken, document: Document
    ):
        access_token.latest_document_at = document.last_updated_at
        self._db.commit()

    def get_shared_documents(
        self,
        access_token: AccessToken,
        page: int = 0,
        size: int = 10,
        share_flags: DocumentShareType = None,
    ):
        query = (
            select(Document)
            .filter(Document.last_updated_at > access_token.latest_document_at)
            .order_by(Document.last_updated_at.asc())
            .offset(page * size)
            .limit(size)
        )

        if share_flags & DocumentTeamTopic.PUBLIC:
            # Return *public* documents
            query = query.filter(Document.is_public.is_(True))
        if share_flags & DocumentTeamTopic.SHARED_WITH_USER:
            # Return documents that have been shared with the user directly
            query = query.join(DocumentUser).filter(
                DocumentUser.user_id == access_token.user_id,
            )
        if share_flags & DocumentTeamTopic.SUBSCRIBED_TEAM:
            # Return documents that have been shared with a team the user
            # subscribed to
            # TODO: mid-term, we
            query = query.join(DocumentTeamTopic).join(TeamTopic).filter()

        ret = list(self._db.scalars(query))
        if ret:
            self._update_user_latest_document(access_token, ret[-1])
        return ret

    def get_my_documents(self, user: User, page: int = 0, size: int = 10):
        return self._db.scalars(
            select(Document)
            .filter(Document.user_id == user.id)
            .order_by(Document.last_updated_at.desc())
            .offset(page * size)
            .limit(size)
        )
