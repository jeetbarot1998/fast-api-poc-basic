"""Add password column

Revision ID: 1323c6bf4d1a
Revises: 13889ea9282a
Create Date: 2023-11-27 22:01:51.913134

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1323c6bf4d1a'
down_revision: Union[str, None] = '13889ea9282a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user_table', sa.Column('password', sa.String(255), nullable=False))


def downgrade() -> None:
    pass
