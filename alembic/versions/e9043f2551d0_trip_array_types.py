"""Trip Array types

Revision ID: e9043f2551d0
Revises: 1829d1d2fb2a
Create Date: 2025-02-07 16:00:48.197830

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e9043f2551d0'
down_revision: Union[str, None] = '1829d1d2fb2a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
