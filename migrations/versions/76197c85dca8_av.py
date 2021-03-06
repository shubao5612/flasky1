"""'av'

Revision ID: 76197c85dca8
Revises: 84d143bde97f
Create Date: 2017-11-14 20:17:41.666000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76197c85dca8'
down_revision = '84d143bde97f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('avatar_hash', sa.String(length=64), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'avatar_hash')
    # ### end Alembic commands ###
