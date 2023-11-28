"""Add new_column manually

Revision ID: 13889ea9282a
Revises: 
Create Date: 2023-11-27 19:58:22.882411

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '13889ea9282a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user_table', sa.Column('email', sa.String(length=100), nullable=True))


def downgrade() -> None:
    pass
