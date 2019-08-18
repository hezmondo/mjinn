"""empty message

Revision ID: 2028b4a4a7ec
Revises: 73fb0d62eb59
Create Date: 2019-08-18 20:39:01.761420

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '2028b4a4a7ec'
down_revision = '73fb0d62eb59'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_foreign_key(None, 'landlord', 'manager', ['manager_id'], ['id'])
    op.create_foreign_key(None, 'landlord', 'typebankacc', ['bankacc_id'], ['id'])
    op.create_foreign_key(None, 'landlord', 'emailaccount', ['emailacc_id'], ['id'])
    op.drop_column('landlord', 'details')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('landlord', sa.Column('details', mysql.VARCHAR(length=90), nullable=True))
    op.drop_constraint(None, 'landlord', type_='foreignkey')
    op.drop_constraint(None, 'landlord', type_='foreignkey')
    op.drop_constraint(None, 'landlord', type_='foreignkey')
    # ### end Alembic commands ###
