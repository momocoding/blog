"""empty message

Revision ID: 72454a78cd13
Revises: None
Create Date: 2016-10-31 23:07:44.220964

"""

# revision identifiers, used by Alembic.
revision = '72454a78cd13'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=30), nullable=True),
    sa.Column('password', sa.String(length=60), nullable=True),
    sa.Column('avatar', sa.String(length=50), nullable=True),
    sa.Column('created_time', sa.String(length=30), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('username')
    )
    op.create_table('blogs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('read_count', sa.Integer(), nullable=True),
    sa.Column('comment_count', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=50), nullable=True),
    sa.Column('sort', sa.String(length=20), nullable=True),
    sa.Column('summary', sa.String(length=150), nullable=True),
    sa.Column('content', sa.String(length=1000), nullable=True),
    sa.Column('created_time', sa.String(length=30), nullable=True),
    sa.Column('user_id', sa.String(length=30), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('comments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('content', sa.String(length=30), nullable=True),
    sa.Column('created_time', sa.String(length=30), nullable=True),
    sa.Column('user_id', sa.String(length=30), nullable=True),
    sa.Column('blog_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['blog_id'], ['blogs.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.username'], ),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comments')
    op.drop_table('blogs')
    op.drop_table('users')
    ### end Alembic commands ###