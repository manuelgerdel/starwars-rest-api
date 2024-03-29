"""empty message

Revision ID: d2fd676f1aa8
Revises: 162588d2d980
Create Date: 2023-08-28 21:08:31.401081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd2fd676f1aa8'
down_revision = '162588d2d980'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('planet',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('population', sa.Integer(), nullable=False),
    sa.Column('rotation_period', sa.String(length=20), nullable=False),
    sa.Column('climate', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('population')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('planet')
    # ### end Alembic commands ###
