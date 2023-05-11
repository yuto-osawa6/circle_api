"""changeForModel

Revision ID: b3d9ffd67d77
Revises: 2aa879fbd4b8
Create Date: 2023-05-10 13:10:53.937779

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'b3d9ffd67d77'
down_revision = '2aa879fbd4b8'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('group_chat_contents', 'group_chat_id',
               existing_type=mysql.INTEGER(),
               nullable=False)
    op.create_unique_constraint(None, 'group_chat_contents', ['group_chat_id'])
    op.create_unique_constraint(None, 'user_details', ['user_id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'user_details', type_='unique')
    op.drop_constraint(None, 'group_chat_contents', type_='unique')
    op.alter_column('group_chat_contents', 'group_chat_id',
               existing_type=mysql.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
