"""empty message

Revision ID: 2d1e2ef3cc21
Revises: 53b47bcd8943
Create Date: 2023-06-29 21:28:29.532585

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2d1e2ef3cc21'
down_revision = '53b47bcd8943'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('picture', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'picture')
    # ### end Alembic commands ###
