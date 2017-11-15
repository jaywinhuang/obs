"""comment

Revision ID: ac1d6db37341
Revises: 1164dc7769bd
Create Date: 2017-11-14 14:01:43.169843

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ac1d6db37341'
down_revision = '1164dc7769bd'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('username', sa.String(length=64), nullable=True))
    op.drop_index('user_name', table_name='user')
    op.create_unique_constraint(None, 'user', ['username'])
    op.drop_column('user', 'user_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('user', sa.Column('user_name', mysql.VARCHAR(length=64), nullable=True))
    op.drop_constraint(None, 'user', type_='unique')
    op.create_index('user_name', 'user', ['user_name'], unique=True)
    op.drop_column('user', 'username')
    # ### end Alembic commands ###
