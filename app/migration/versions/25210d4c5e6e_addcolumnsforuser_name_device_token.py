"""AddColumnsForUser name:device_token

Revision ID: 25210d4c5e6e
Revises: b5c98bdcccff
Create Date: 2023-06-30 04:43:53.236151

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.orm import Session
# import app.models.user
from sqlalchemy import func
# from app.models.user import User
from app.models.user import User
from app.db import Base


# revision identifiers, used by Alembic.
revision = '25210d4c5e6e'
down_revision = 'b5c98bdcccff'
branch_labels = None
depends_on = None


def upgrade() -> None:
    bind = op.get_bind()
    session = Session(bind=bind)
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('device_token', sa.String(length=768), nullable=False))
    set_unique_device_tokens(session)
    op.create_unique_constraint(None, 'users', ['device_token'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    # op.drop_constraint(None, 'users', type_='unique')
    op.drop_column('users', 'device_token')
    # ### end Alembic commands ###

def set_unique_device_tokens(db: Session) -> None:
    try:
        print(db)
        print("aaa")
        print(User)
        users2 = db.query(User).all()
        print(users2)
        users = db.query(User).filter(User.device_token.is_(None)).all()
        # # existing_device_tokens = db.query(User.device_token).distinct().scalar_all()

        # for user in users:
        #     # device_token = generate_unique_device_token(existing_device_tokens)
        #     user.device_token =  str(user.id)
        #     # existing_device_tokens.append(user.id)

        # db.commit()
    except Exception as err:
        print(err)
