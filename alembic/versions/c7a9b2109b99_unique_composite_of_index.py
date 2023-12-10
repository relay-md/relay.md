# -*- coding: utf-8 -*-
"""unique-composite-of-index

Revision ID: c7a9b2109b99
Revises: 08768fd5fc3b
Create Date: 2023-12-08 14:08:43.427331

"""
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

from alembic import op

# revision identifiers, used by Alembic.
revision = "c7a9b2109b99"
down_revision = "08768fd5fc3b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_table('team_member')
    op.create_index(
        "user_team_idx_unique", "user_team", ["user_id", "team_id"], unique=True
    )
    op.create_index(
        "user_team_topics_idx_unique",
        "user_team_topics",
        ["user_id", "team_topic_id"],
        unique=True,
    )
    op.create_index(
        "user_oauth_index_unique", "user", ["username", "oauth_provider"], unique=True
    )
    op.drop_index("user_oauth_index", table_name="user")
    op.drop_index("user_team_idx", table_name="user_team")
    op.drop_index("user_team_topics_idx", table_name="user_team_topics")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("user_team_topics_idx_unique", table_name="user_team_topics")
    op.create_index(
        "user_team_topics_idx",
        "user_team_topics",
        ["user_id", "team_topic_id"],
        unique=False,
    )
    op.drop_index("user_team_idx_unique", table_name="user_team")
    op.create_index("user_team_idx", "user_team", ["user_id", "team_id"], unique=False)
    op.drop_index("user_oauth_index_unique", table_name="user")
    op.create_index(
        "user_oauth_index", "user", ["username", "oauth_provider"], unique=False
    )
    op.create_table(
        "team_member",
        sa.Column("id", mysql.CHAR(length=32), nullable=False),
        sa.Column("team_id", mysql.CHAR(length=32), nullable=False),
        sa.Column("user_id", mysql.CHAR(length=32), nullable=False),
        sa.Column(
            "is_owner",
            mysql.TINYINT(display_width=1),
            autoincrement=False,
            nullable=False,
        ),
        sa.Column(
            "is_moderator",
            mysql.TINYINT(display_width=1),
            autoincrement=False,
            nullable=False,
        ),
        sa.ForeignKeyConstraint(["team_id"], ["team.id"], name="team_member_ibfk_1"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], name="team_member_ibfk_2"),
        sa.PrimaryKeyConstraint("id"),
        mysql_collate="utf8mb4_unicode_ci",
        mysql_default_charset="utf8mb4",
        mysql_engine="InnoDB",
    )
    # ### end Alembic commands ###