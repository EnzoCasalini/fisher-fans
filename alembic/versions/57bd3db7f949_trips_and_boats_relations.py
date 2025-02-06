"""Trips and Boats relations

Revision ID: 57bd3db7f949
Revises: b591f7fde893
Create Date: 2025-02-06 19:48:55.611997

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '57bd3db7f949'
down_revision: Union[str, None] = 'b591f7fde893'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
