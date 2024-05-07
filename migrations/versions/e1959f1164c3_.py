"""empty message

Revision ID: e1959f1164c3
Revises: 6565132ebc19
Create Date: 2024-05-07 09:40:17.625796

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = 'e1959f1164c3'
down_revision: Union[str, None] = '6565132ebc19'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('isActive', sa.Boolean(), server_default='True', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'isActive')
    # ### end Alembic commands ###
