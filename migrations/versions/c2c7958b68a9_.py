"""empty message

Revision ID: c2c7958b68a9
Revises: 3762654a3201
Create Date: 2023-08-29 18:15:40.403334

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c2c7958b68a9'
down_revision = '3762654a3201'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.alter_column('character_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('planet_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.alter_column('planet_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('character_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
