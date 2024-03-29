"""empty message

Revision ID: 25959a9b2c4d
Revises: 
Create Date: 2023-10-20 10:53:27.593621

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '25959a9b2c4d'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('message',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('message_id', sa.String(length=50), nullable=True),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('show', sa.Boolean(), nullable=True),
    sa.Column('duration', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.Column('message', sa.String(length=500), nullable=False),
    sa.Column('dynamic', sa.Boolean(), nullable=True),
    sa.Column('object', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('message_id')
    )
    op.create_table('phan_loai',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('key', sa.Text(), nullable=True),
    sa.Column('name', sa.Text(collation='utf8mb4_unicode_ci'), nullable=True),
    sa.Column('parent_id', sa.String(length=50), nullable=True),
    sa.ForeignKeyConstraint(['parent_id'], ['phan_loai.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('birthday', sa.Date(), nullable=True),
    sa.Column('password', sa.String(length=100), nullable=True),
    sa.Column('name_user', sa.Text(collation='utf8mb4_unicode_ci'), nullable=True),
    sa.Column('phone_number', sa.String(length=100), nullable=True),
    sa.Column('address', sa.Text(collation='utf8mb4_unicode_ci'), nullable=True),
    sa.Column('gender', sa.Boolean(), nullable=True),
    sa.Column('admin', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.Integer(), nullable=True),
    sa.Column('picture', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('user_id', sa.String(length=50), nullable=True),
    sa.Column('phone_number', sa.String(length=100), nullable=True),
    sa.Column('address', sa.Text(collation='utf8mb4_unicode_ci'), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('created_date', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('product',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('name', sa.Text(collation='utf8mb4_unicode_ci'), nullable=True),
    sa.Column('price', sa.Integer(), nullable=True),
    sa.Column('describe', sa.Text(collation='utf8mb4_unicode_ci'), nullable=True),
    sa.Column('phan_loai_id', sa.String(length=50), nullable=True),
    sa.Column('created_date', sa.Integer(), nullable=True),
    sa.Column('picture', sa.Text(), nullable=True),
    sa.Column('old_price', sa.Integer(), nullable=True),
    sa.Column('giam_gia', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['phan_loai_id'], ['phan_loai.id'], onupdate='SET NULL', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('cart_items',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('product_id', sa.String(length=50), nullable=True),
    sa.Column('user_id', sa.String(length=50), nullable=True),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('size', sa.String(length=5), nullable=True),
    sa.Column('color', sa.String(length=50, collation='utf8mb4_unicode_ci'), nullable=True),
    sa.Column('created_date', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('order_items',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('product_id', sa.String(length=50), nullable=True),
    sa.Column('order_id', sa.String(length=50), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=True),
    sa.Column('count', sa.Integer(), nullable=True),
    sa.Column('size', sa.String(length=5), nullable=True),
    sa.Column('color', sa.String(length=50), nullable=True),
    sa.Column('created_date', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['order_id'], ['orders.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], onupdate='SET NULL', ondelete='SET NULL'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reviews',
    sa.Column('id', sa.String(length=50), nullable=False),
    sa.Column('product_id', sa.String(length=50), nullable=True),
    sa.Column('user_id', sa.String(length=50), nullable=True),
    sa.Column('comment', sa.Text(collation='utf8mb4_unicode_ci'), nullable=True),
    sa.Column('created_date', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['product_id'], ['product.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reviews')
    op.drop_table('order_items')
    op.drop_table('cart_items')
    op.drop_table('product')
    op.drop_table('orders')
    op.drop_table('user')
    op.drop_table('phan_loai')
    op.drop_table('message')
    # ### end Alembic commands ###
