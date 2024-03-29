"""Intial tables

Revision ID: c838af0963e0
Revises: 
Create Date: 2023-03-07 10:53:26.484795

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c838af0963e0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('plates',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('hour', sa.String(length=10), nullable=False),
    sa.Column('plate', sa.String(length=10), nullable=False),
    sa.Column('image', sa.String(length=100), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('password', sa.String(length=20), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('admin', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('plates')
    # ### end Alembic commands ###
