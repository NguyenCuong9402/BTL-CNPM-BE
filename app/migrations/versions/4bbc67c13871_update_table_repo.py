"""update table repo

Revision ID: 4bbc67c13871
Revises: 9b8e951dbb97
Create Date: 2022-07-12 16:44:53.585025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4bbc67c13871'
down_revision = '9b8e951dbb97'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test_repo', sa.Column('project_id', sa.String(length=50), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('test_repo', 'project_id')
    # ### end Alembic commands ###