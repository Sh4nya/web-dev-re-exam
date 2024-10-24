"""Fix field names

Revision ID: 987ac3f81936
Revises: c551129b6671
Create Date: 2024-06-03 16:10:44.589495

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '987ac3f81936'
down_revision = 'c551129b6671'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('title', sa.String(length=255), nullable=False))
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=False))
        batch_op.drop_column('short_desc')
        batch_op.drop_column('name')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name', mysql.VARCHAR(length=255), nullable=False))
        batch_op.add_column(sa.Column('short_desc', mysql.TEXT(), nullable=False))
        batch_op.drop_column('description')
        batch_op.drop_column('title')

    # ### end Alembic commands ###
