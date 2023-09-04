"""empty message

Revision ID: 3762654a3201
Revises: 23a80941ce3b
Create Date: 2023-08-29 17:44:06.765204

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3762654a3201'
down_revision = '23a80941ce3b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.alter_column('character_id',
               existing_type=sa.INTEGER(),
               nullable=False)
        batch_op.alter_column('planet_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.alter_column('planet_id',
               existing_type=sa.INTEGER(),
               nullable=True)
        batch_op.alter_column('character_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###
