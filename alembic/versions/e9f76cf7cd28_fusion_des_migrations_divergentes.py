"""Fusion des migrations divergentes

Revision ID: e9f76cf7cd28
Revises: 6d21b8703408, d4b527b727cd
Create Date: 2025-02-22 16:59:22.487785

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9f76cf7cd28'
down_revision: Union[str, None] = ('6d21b8703408', 'd4b527b727cd')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
