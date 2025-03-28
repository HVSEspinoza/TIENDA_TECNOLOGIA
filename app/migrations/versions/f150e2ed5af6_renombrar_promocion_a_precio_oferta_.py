"""Renombrar promocion a precio_oferta_compra_usd y añadir precio_oferta_compra_soles

Revision ID: f150e2ed5af6
Revises: c14c070ae470
Create Date: 2025-03-14 17:02:35.553315

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f150e2ed5af6'
down_revision = 'c14c070ae470'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('producto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('precio_compra_usd', sa.Numeric(precision=10, scale=2), nullable=False))
        batch_op.add_column(sa.Column('precio_compra_soles', sa.Numeric(precision=10, scale=2), nullable=False))
        batch_op.add_column(sa.Column('precio_oferta_compra_usd', sa.Numeric(precision=10, scale=2), nullable=True))
        batch_op.add_column(sa.Column('precio_oferta_compra_soles', sa.Numeric(precision=10, scale=2), nullable=True))
        batch_op.drop_column('precio_soles')
        batch_op.drop_column('promocion')
        batch_op.drop_column('precio_dolares')

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('producto', schema=None) as batch_op:
        batch_op.add_column(sa.Column('precio_dolares', mysql.DECIMAL(precision=10, scale=2), nullable=False))
        batch_op.add_column(sa.Column('promocion', mysql.DECIMAL(precision=10, scale=2), nullable=True))
        batch_op.add_column(sa.Column('precio_soles', mysql.DECIMAL(precision=10, scale=2), nullable=False))
        batch_op.drop_column('precio_oferta_compra_soles')
        batch_op.drop_column('precio_oferta_compra_usd')
        batch_op.drop_column('precio_compra_soles')
        batch_op.drop_column('precio_compra_usd')

    # ### end Alembic commands ###
