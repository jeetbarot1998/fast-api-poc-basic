"""add token field to user_location table

Revision ID: 5a773ecbdf10
Revises: c2c194b0a4a0
Create Date: 2023-11-28 02:30:25.995499

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5a773ecbdf10'
down_revision: Union[str, None] = 'c2c194b0a4a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user_location', sa.Column('token', sa.String(100), nullable=False))


def downgrade() -> None:
    op.drop_column('user_location', 'token')
