"""add_article_type_to_categories

Revision ID: a9f3c1e7d205
Revises: 4136f276b49d
Create Date: 2026-05-06 09:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = 'a9f3c1e7d205'
down_revision: Union[str, None] = '4136f276b49d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('categories', sa.Column('article_type', sa.Integer(), nullable=False, server_default='1'))


def downgrade() -> None:
    op.drop_column('categories', 'article_type')
