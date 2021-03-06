"""remove-user-fields

Revision ID: 6213f28505cc
Revises: a4582037ad86
Create Date: 2017-05-24 12:57:14.134293

"""

# revision identifiers, used by Alembic.
revision = '6213f28505cc'
down_revision = 'a4582037ad86'
branch_labels = None
depends_on = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('resetlinks', 'tenancy')
    op.drop_constraint(u'users_activation_link_key', 'users', type_='unique')
    op.drop_column('users', 'activation_link')
    op.drop_column('users', 'first_name')
    op.drop_column('users', 'last_name')
    op.drop_column('users', 'activated')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('activated', sa.BOOLEAN(), autoincrement=False, nullable=False))
    op.add_column('users', sa.Column('last_name', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('first_name', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.add_column('users', sa.Column('activation_link', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.create_unique_constraint(u'users_activation_link_key', 'users', ['activation_link'])
    op.add_column('resetlinks', sa.Column('tenancy', sa.VARCHAR(length=120), autoincrement=False, nullable=False))
    ### end Alembic commands ###
