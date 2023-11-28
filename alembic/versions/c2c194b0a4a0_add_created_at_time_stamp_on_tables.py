"""add created at time stamp on tables

Revision ID: c2c194b0a4a0
Revises: bdd3e7059ced
Create Date: 2023-11-28 01:12:07.515071

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c2c194b0a4a0'
down_revision: Union[str, None] = 'bdd3e7059ced'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user_table', sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()))
    op.add_column('user_table', sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now()))
    op.add_column('user_location', sa.Column('created_at', sa.TIMESTAMP, server_default=sa.func.now()))
    op.add_column('user_location', sa.Column('updated_at', sa.TIMESTAMP, server_default=sa.func.now(), onupdate=sa.func.now()))


def downgrade() -> None:
    op.drop_column('user_table','created_at')
    op.drop_column('user_table','updated_at')
    op.drop_column('user_location','created_at')
    op.drop_column('user_location','updated_at')
