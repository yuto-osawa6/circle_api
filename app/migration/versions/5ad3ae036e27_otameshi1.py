"""otameshi1

Revision ID: 5ad3ae036e27
Revises: 1b0e4b3cd367
Create Date: 2023-04-01 09:18:16.908790

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '5ad3ae036e27'
down_revision = '1b0e4b3cd367'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('atasks', sa.Column('title5', sa.String(length=1024), nullable=True))
    op.alter_column('users', 'uid',
               existing_type=mysql.VARCHAR(length=768),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'uid',
               existing_type=mysql.VARCHAR(length=768),
               nullable=True)
    op.drop_column('atasks', 'title5')
    # ### end Alembic commands ###
