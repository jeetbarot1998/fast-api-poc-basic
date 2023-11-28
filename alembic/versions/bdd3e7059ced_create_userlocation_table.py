"""Create UserLocation table

Revision ID: bdd3e7059ced
Revises: 1323c6bf4d1a
Create Date: 2023-11-28 01:07:12.090713

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bdd3e7059ced'
down_revision: Union[str, None] = '1323c6bf4d1a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'user_location',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('longitude', sa.DECIMAL(10, 8)),
        sa.Column('latitude', sa.DECIMAL(10, 8)),
        sa.Column('map_id', sa.Integer, sa.ForeignKey('user_table.id'))
    )


def downgrade() -> None:
    op.drop_table('user_location')
