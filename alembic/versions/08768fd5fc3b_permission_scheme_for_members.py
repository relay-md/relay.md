# -*- coding: utf-8 -*-
"""permission scheme for members

Revision ID: 08768fd5fc3b
Revises: 7d13db2365c5
Create Date: 2023-12-08 10:53:41.130100

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "08768fd5fc3b"
down_revision = "7d13db2365c5"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "user_team", sa.Column("can_invite_users", sa.Boolean(), nullable=False)
    )
    op.add_column(
        "user_team", sa.Column("can_post_documents", sa.Boolean(), nullable=False)
    )
    op.add_column(
        "user_team", sa.Column("can_delete_documents", sa.Boolean(), nullable=False)
    )
    op.add_column(
        "user_team", sa.Column("can_modify_documents", sa.Boolean(), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("user_team", "can_modify_documents")
    op.drop_column("user_team", "can_delete_documents")
    op.drop_column("user_team", "can_post_documents")
    op.drop_column("user_team", "can_invite_users")
    # ### end Alembic commands ###