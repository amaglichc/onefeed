"""empty message

Revision ID: cad1c7a6ebae
Revises: fdf3b1727bd8
Create Date: 2024-05-11 13:06:16.672609

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'cad1c7a6ebae'
down_revision: Union[str, None] = 'fdf3b1727bd8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('comments', sa.Column('likes', sa.Integer(), server_default='0', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('comments', 'likes')
    # ### end Alembic commands ###
