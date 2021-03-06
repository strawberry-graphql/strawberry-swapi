"""empty message

Revision ID: 23f69436a28d
Revises: 5a8987aaa87b
Create Date: 2019-04-20 11:32:40.831995

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '23f69436a28d'
down_revision = '5a8987aaa87b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('people', sa.Column('homeworld_id', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('people', 'homeworld_id')
    # ### end Alembic commands ###
