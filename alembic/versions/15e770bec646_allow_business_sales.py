# -*- coding: utf-8 -*-
"""allow-business-sales

Revision ID: 15e770bec646
Revises: d8956460586b
Create Date: 2024-02-15 11:05:42.136675

"""
import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision = "15e770bec646"
down_revision = "d8956460586b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "billing_person", sa.Column("vat_id", sa.String(length=128), nullable=True)
    )
    op.add_column(
        "billing_person", sa.Column("is_business", sa.Boolean(), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("billing_person", "is_business")
    op.drop_column("billing_person", "vat_id")
    # ### end Alembic commands ###
