"""empty message

Revision ID: 6771d2304bea
Revises: 
Create Date: 2024-03-17 14:30:11.157153

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6771d2304bea'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('userid', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=True),
    sa.Column('password_hash', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('userid')
    )
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)
        batch_op.create_index(batch_op.f('ix_user_username'), ['username'], unique=True)

    op.create_table('post',
    sa.Column('postid', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['userid'], ['user.userid'], ),
    sa.PrimaryKeyConstraint('postid')
    )
    op.create_table('comment',
    sa.Column('commentid', sa.Integer(), nullable=False),
    sa.Column('postid', sa.Integer(), nullable=True),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('content', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['postid'], ['post.postid'], ),
    sa.ForeignKeyConstraint(['userid'], ['user.userid'], ),
    sa.PrimaryKeyConstraint('commentid')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('comment')
    op.drop_table('post')
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_username'))
        batch_op.drop_index(batch_op.f('ix_user_email'))

    op.drop_table('user')
    # ### end Alembic commands ###
