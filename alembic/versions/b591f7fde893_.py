"""empty message

Revision ID: b591f7fde893
Revises: 2132fcc6ad20, 607d0b7e50d9
Create Date: 2025-02-06 19:48:33.358171

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b591f7fde893'
down_revision: Union[str, None] = ('2132fcc6ad20', '607d0b7e50d9')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
