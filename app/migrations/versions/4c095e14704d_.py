"""empty message

Revision ID: 4c095e14704d
Revises: 25959a9b2c4d
Create Date: 2023-10-21 16:55:55.838576

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4c095e14704d'
down_revision = '25959a9b2c4d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('cac_mau', sa.JSON(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'cac_mau')
    # ### end Alembic commands ###
