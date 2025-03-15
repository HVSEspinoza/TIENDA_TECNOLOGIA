"""Add categoria_general and subcategoria to Producto

Revision ID: c6e4508b53d3
Revises: f150e2ed5af6
Create Date: 2025-03-15 16:11:24.340058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c6e4508b53d3'
down_revision = 'f150e2ed5af6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('producto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('categoria_general', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('subcategoria', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('producto', schema=None) as batch_op:
        batch_op.drop_column('subcategoria')
        batch_op.drop_column('categoria_general')

    # ### end Alembic commands ###
