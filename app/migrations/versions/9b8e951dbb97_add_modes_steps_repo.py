"""add modes steps repo

Revision ID: 9b8e951dbb97
Revises: ff927e5d4b72
Create Date: 2022-07-12 14:58:08.772473

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '9b8e951dbb97'
down_revision = 'ff927e5d4b72'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('project_setting',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('description', sa.Integer(), nullable=True),
    sa.Column('project_name', sa.String(length=255), nullable=True),
    sa.Column('project_id', sa.String(length=255), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('test_repo',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('parent_id', sa.String(length=50), nullable=False),
    sa.Column('name', sa.String(length=500), nullable=True),
    sa.Column('create_date', mysql.INTEGER(unsigned=True), nullable=True),
    sa.PrimaryKeyConstraint('id', 'parent_id')
    )
    op.create_index(op.f('ix_test_repo_create_date'), 'test_repo', ['create_date'], unique=False)
    op.create_table('test_field',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('key', sa.Integer(), autoincrement=True, nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('project_setting_id', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['project_setting_id'], ['project_setting.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('test_steps_config',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('key', sa.Integer(), autoincrement=True, nullable=True),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('project_setting_id', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['project_setting_id'], ['project_setting.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('map_test_repo',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('test_id', sa.String(length=50), nullable=True),
    sa.Column('test_repo_id', sa.String(length=50), nullable=True),
    sa.Column('create_date', mysql.INTEGER(unsigned=True), nullable=True),
    sa.ForeignKeyConstraint(['test_id'], ['tests.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.ForeignKeyConstraint(['test_repo_id'], ['test_repo.id'], onupdate='CASCADE', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_map_test_repo_create_date'), 'map_test_repo', ['create_date'], unique=False)
    op.create_index(op.f('ix_map_test_repo_test_id'), 'map_test_repo', ['test_id'], unique=False)
    op.create_index(op.f('ix_map_test_repo_test_repo_id'), 'map_test_repo', ['test_repo_id'], unique=False)
    op.create_foreign_key(None, 'test_type', 'project_setting', ['project_setting_id'], ['id'], onupdate='CASCADE', ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'test_type', type_='foreignkey')
    op.drop_index(op.f('ix_map_test_repo_test_repo_id'), table_name='map_test_repo')
    op.drop_index(op.f('ix_map_test_repo_test_id'), table_name='map_test_repo')
    op.drop_index(op.f('ix_map_test_repo_create_date'), table_name='map_test_repo')
    op.drop_table('map_test_repo')
    op.drop_table('test_steps_config')
    op.drop_table('test_field')
    op.drop_index(op.f('ix_test_repo_create_date'), table_name='test_repo')
    op.drop_table('test_repo')
    op.drop_table('project_setting')
    # ### end Alembic commands ###
