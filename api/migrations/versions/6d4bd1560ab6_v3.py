"""v3

Revision ID: 6d4bd1560ab6
Revises: e186c0bd9520
Create Date: 2021-07-09 14:48:43.196165

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d4bd1560ab6'
down_revision = 'e186c0bd9520'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('classifications',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('is_delete', sa.BOOLEAN(), nullable=True),
    sa.Column('create_time', sa.DATETIME(timezone=6), nullable=True),
    sa.Column('update_time', sa.DATETIME(timezone=6), nullable=True),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('rank', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_unique_constraint(None, 'products', ['no'])
    op.create_unique_constraint(None, 'products', ['name'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'products', type_='unique')
    op.drop_constraint(None, 'products', type_='unique')
    op.drop_table('classifications')
    # ### end Alembic commands ###
