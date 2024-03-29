"""create_chat_model

Revision ID: 2aa879fbd4b8
Revises: 920978b45423
Create Date: 2023-04-18 12:11:20.755567

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2aa879fbd4b8'
down_revision = '920978b45423'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('group_chat_contents',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('group_chat_id', sa.Integer(), nullable=True),
    sa.Column('content_type', sa.String(length=20), nullable=False),
    sa.Column('s3_object_key', sa.Text(), nullable=True),
    sa.Column('text_content', sa.Text(length=2000), nullable=True),
    sa.ForeignKeyConstraint(['group_chat_id'], ['group_chats.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_group_chat_contents_id'), 'group_chat_contents', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_group_chat_contents_id'), table_name='group_chat_contents')
    op.drop_table('group_chat_contents')
    # ### end Alembic commands ###
