"""Merge conflicting migrations

Revision ID: ab91875035e5
Revises: 6d21b8703408, d4b527b727cd
Create Date: 2025-02-22 17:04:46.007444

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ab91875035e5'
down_revision: Union[str, None] = ('6d21b8703408', 'd4b527b727cd')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
