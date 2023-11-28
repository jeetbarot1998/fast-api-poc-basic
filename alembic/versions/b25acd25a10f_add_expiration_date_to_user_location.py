"""add expiration date to user_location

Revision ID: b25acd25a10f
Revises: 5a773ecbdf10
Create Date: 2023-11-28 02:36:26.568299

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b25acd25a10f'
down_revision: Union[str, None] = '5a773ecbdf10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('user_location', sa.Column('expiration_time', sa.DateTime(), nullable=True))

def downgrade() -> None:
    op.drop_column('user_location','expiration_time')
