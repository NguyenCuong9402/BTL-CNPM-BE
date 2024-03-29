"""empty message

Revision ID: 2ebabdfba7cc
Revises: 4c095e14704d
Create Date: 2023-10-25 10:47:20.232478

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ebabdfba7cc'
down_revision = '4c095e14704d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dia_chi',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('tinh', sa.Text(collation='utf8mb4_unicode_ci'), nullable=True),
    sa.Column('huyen', sa.Text(collation='utf8mb4_unicode_ci'), nullable=True),
    sa.Column('xa', sa.Text(collation='utf8mb4_unicode_ci'), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dia_chi')
    # ### end Alembic commands ###
