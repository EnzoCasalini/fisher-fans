"""empty message

Revision ID: b67ff50b9920
Revises: 0afb78cd7f1c, ab8d05811e3c, e9043f2551d0
Create Date: 2025-02-24 09:35:00.018084

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b67ff50b9920'
down_revision: Union[str, None] = ('0afb78cd7f1c', 'ab8d05811e3c', 'e9043f2551d0')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
