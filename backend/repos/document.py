# -*- coding: utf-8 -*-
from typing import List, Optional

from sqlalchemy import func, or_, select

from ..config import get_config
from ..models.access_token import AccessToken
from ..models.document import Document
from ..models.document_team_topic import DocumentTeamTopic
from ..models.document_user import DocumentUser
from ..models.team_topic import TeamTopic
from ..models.user import User
from ..models.user_team_topic import UserTeamTopic
from ..schema import DocumentShareType
from .base import DatabaseAbstractRepository

# TODO: reduce duplicate code w.r.t. *_count and DocumentShareType


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
        share_flags: Optional[DocumentShareType] = None,
    ):
        query = (
            select(Document)
            .filter(Document.last_updated_at > access_token.latest_document_at)
            .order_by(Document.last_updated_at.asc())
            .offset(page * size)
            .limit(size)
        )

        filters = list()
        if share_flags and share_flags & DocumentShareType.PUBLIC:
            # Return *public* documents
            filters.append(Document.is_public.is_(True))

        # Below, we need OUTER JOIN because a document can be shared either by
        # team topic or by user and we do not want to miss one of them by
        # requiring the other through an inner join!
        if share_flags and share_flags & DocumentShareType.SHARED_WITH_USER:
            # Return documents that have been shared with the user directly
            query = query.outerjoin(DocumentUser)
            filters.append(
                DocumentUser.user_id == access_token.user_id,
            )

        if share_flags and share_flags & DocumentShareType.SUBSCRIBED_TEAM:
            # Return documents that have been shared with a team the user
            # subscribed to
            query = (
                query.outerjoin(DocumentTeamTopic)
                .outerjoin(TeamTopic)
                .outerjoin(UserTeamTopic)
            )
            filters.append(
                UserTeamTopic.user_id == access_token.user_id,
            )

        query = query.filter(or_(*[x for x in filters]))
        ret = list(self._db.scalars(query))
        if ret:
            self._update_user_latest_document(access_token, ret[-1])
        return ret

    def get_shared_documents_for_user(
        self,
        user: User,
        page: int = 0,
        size: int = 10,
        share_flags: DocumentShareType = DocumentShareType.PUBLIC
        | DocumentShareType.SHARED_WITH_USER
        | DocumentShareType.SUBSCRIBED_TEAM,
    ):
        query = (
            select(Document)
            .order_by(Document.last_updated_at.asc())
            .filter(Document.user_id != user.id)  # not owned by us
        )

        filters = list()
        if share_flags and share_flags & DocumentShareType.PUBLIC:
            # Return *public* documents
            filters.append(Document.is_public.is_(True))

        # Below, we need OUTER JOIN because a document can be shared either by
        # team topic or by user and we do not want to miss one of them by
        # requiring the other through an inner join!
        if share_flags and share_flags & DocumentShareType.SHARED_WITH_USER:
            # Return documents that have been shared with the user directly
            query = query.outerjoin(DocumentUser)
            filters.append(
                DocumentUser.user_id == user.id,
            )

        if share_flags and share_flags & DocumentShareType.SUBSCRIBED_TEAM:
            # Return documents that have been shared with a team the user
            # subscribed to
            query = (
                query.outerjoin(DocumentTeamTopic)
                .outerjoin(TeamTopic)
                .outerjoin(UserTeamTopic)
            )
            filters.append(
                UserTeamTopic.user_id == user.id,
            )

        query = query.filter(or_(*[x for x in filters]))
        query = query.offset(page * size).limit(size)
        return list(self._db.scalars(query))

    def get_shared_documents_for_user_count(
        self,
        user: User,
        share_flags: DocumentShareType = DocumentShareType.PUBLIC
        | DocumentShareType.SHARED_WITH_USER
        | DocumentShareType.SUBSCRIBED_TEAM,
    ):
        query = select(func.count(Document.id)).filter(
            Document.user_id != user.id
        )  # not owned by us

        filters = list()
        if share_flags and share_flags & DocumentShareType.PUBLIC:
            # Return *public* documents
            filters.append(Document.is_public.is_(True))

        # Below, we need OUTER JOIN because a document can be shared either by
        # team topic or by user and we do not want to miss one of them by
        # requiring the other through an inner join!
        if share_flags and share_flags & DocumentShareType.SHARED_WITH_USER:
            # Return documents that have been shared with the user directly
            query = query.outerjoin(DocumentUser)
            filters.append(
                DocumentUser.user_id == user.id,
            )

        if share_flags and share_flags & DocumentShareType.SUBSCRIBED_TEAM:
            # Return documents that have been shared with a team the user
            # subscribed to
            query = (
                query.outerjoin(DocumentTeamTopic)
                .outerjoin(TeamTopic)
                .outerjoin(UserTeamTopic)
            )
            filters.append(
                UserTeamTopic.user_id == user.id,
            )

        query = query.filter(or_(*[x for x in filters]))
        return self._db.scalar(query)

    def get_my_documents(self, user: User, page: int = 0, size: int = 10):
        return list(
            self._db.scalars(
                select(Document)
                .filter(Document.user_id == user.id)
                .order_by(Document.last_updated_at.desc())
                .offset(page * size)
                .limit(size)
            )
        )

    def get_my_documents_count(self, user: User):
        return self._db.scalar(
            select(func.count(Document.id)).filter(Document.user_id == user.id)
        )

    def latest_news(self, size=10) -> List[Document]:
        if not get_config().RELAY_NEWS_TEAM_TOPIC_ID:
            return []
        return list(
            self._db.scalars(
                select(Document)
                .filter(
                    Document.team_topics.any(
                        TeamTopic.id == get_config().RELAY_NEWS_TEAM_TOPIC_ID
                    )
                )
                .order_by(Document.last_updated_at.desc())
                .limit(size)
            )
        )

    def list_from_team_topic(
        self, team_topic: TeamTopic, size, page: int
    ) -> List[Document]:
        return list(
            self._db.scalars(
                select(Document)
                .filter(Document.team_topics.any(TeamTopic.id == team_topic.id))
                .order_by(Document.last_updated_at.desc())
                .limit(size)
            )
        )
