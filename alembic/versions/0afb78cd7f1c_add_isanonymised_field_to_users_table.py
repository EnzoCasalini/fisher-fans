"""Add isAnonymised field to users table

Revision ID: 0afb78cd7f1c
Revises: 80c1a07ba518
Create Date: 2025-02-22 17:52:46.718686

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0afb78cd7f1c'
down_revision: Union[str, None] = '80c1a07ba518'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('isAnonymised', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'isAnonymised')
    # ### end Alembic commands ###
