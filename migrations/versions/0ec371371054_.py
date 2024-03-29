"""empty message

Revision ID: 0ec371371054
Revises: 934ffac8d339
Create Date: 2023-09-02 14:11:33.246513

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0ec371371054'
down_revision = '934ffac8d339'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.drop_constraint('favorite_character_id_key', type_='unique')
        batch_op.drop_constraint('favorite_planet_id_key', type_='unique')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('favorite', schema=None) as batch_op:
        batch_op.create_unique_constraint('favorite_planet_id_key', ['planet_id'])
        batch_op.create_unique_constraint('favorite_character_id_key', ['character_id'])

    # ### end Alembic commands ###
