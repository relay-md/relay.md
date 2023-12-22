# -*- coding: utf-8 -*-
"""allow-hide-team

Revision ID: 9a233ea067ef
Revises: 3911c02d6c45
Create Date: 2023-12-22 14:34:35.177137

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "9a233ea067ef"
down_revision = "3911c02d6c45"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column("team", sa.Column("hide", sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("team", "hide")
    # ### end Alembic commands ###
