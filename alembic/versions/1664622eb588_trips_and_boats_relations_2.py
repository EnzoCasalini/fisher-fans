"""Trips and Boats relations 2

Revision ID: 1664622eb588
Revises: 57bd3db7f949
Create Date: 2025-02-06 19:52:10.723068

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1664622eb588'
down_revision: Union[str, None] = '57bd3db7f949'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Use batch operations for SQLite
    with op.batch_alter_table('trips') as batch_op:
        batch_op.add_column(sa.Column('boat_id', sa.String(), nullable=True))
        batch_op.create_foreign_key('fk_trips_boat_id', 'boats', ['boat_id'], ['id'])


def downgrade() -> None:
    # Use batch operations for SQLite
    with op.batch_alter_table('trips') as batch_op:
        batch_op.drop_constraint('fk_trips_boat_id', type_='foreignkey')
        batch_op.drop_column('boat_id')

