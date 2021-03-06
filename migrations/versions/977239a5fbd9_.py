"""empty message

Revision ID: 977239a5fbd9
Revises: 
Create Date: 2020-08-23 16:15:13.313371

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '977239a5fbd9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('ih_orders_ibfk_2', 'ih_orders', type_='foreignkey')
    op.create_foreign_key(None, 'ih_orders', 'ih_users', ['user_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'ih_orders', type_='foreignkey')
    op.create_foreign_key('ih_orders_ibfk_2', 'ih_orders', 'ih_orders', ['user_id'], ['id'])
    # ### end Alembic commands ###
