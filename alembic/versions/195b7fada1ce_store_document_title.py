# -*- coding: utf-8 -*-
"""store-document title

Revision ID: 195b7fada1ce
Revises: b86be333d9be
Create Date: 2023-12-06 14:30:29.148763

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "195b7fada1ce"
down_revision = "b86be333d9be"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("document", sa.Column("title", sa.String(length=256), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("document", "title")
    # ### end Alembic commands ###