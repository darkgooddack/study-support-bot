"""Create users table

Revision ID: d384fdbd961a
Revises: d954356e7481
Create Date: 2024-12-16 12:43:45.583935

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd384fdbd961a'
down_revision: Union[str, None] = 'd954356e7481'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('telegram_id', sa.BigInteger(), nullable=False),
    sa.Column('username', sa.String(), nullable=True),
    sa.Column('role', sa.String(), nullable=True),
    sa.Column('direction', sa.String(), nullable=True),
    sa.Column('about', sa.String(), nullable=True),
    sa.Column('github', sa.String(), nullable=True),
    sa.Column('linkedin', sa.String(), nullable=True),
    sa.Column('visibility', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    # ### end Alembic commands ###
