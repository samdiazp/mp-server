"""empty message

Revision ID: 68209e71d9dc
Revises: 476260aedc8d
Create Date: 2023-03-07 15:17:23.630595

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime


# revision identifiers, used by Alembic.
revision = '68209e71d9dc'
down_revision = '476260aedc8d'
branch_labels = None
depends_on = None


def upgrade() -> None:
     op.create_table("products",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("name", sa.String),
        sa.Column("price", sa.Float),
        sa.Column("benefits", sa.String),
        sa.Column('created_at', sa.DateTime, default=datetime.now()),
        sa.Column('updated_at', sa.DateTime)
    )
     op.create_table("orders",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("total", sa.Float),
        sa.Column("status", sa.Integer),
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id")),
        sa.Column("sites_id", sa.Integer, sa.ForeignKey("sites.id")),
        sa.Column("date", sa.DateTime, nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.now()),
        sa.Column('updated_at', sa.DateTime)
    )
     op.create_table("order_products",
        sa.Column("id", sa.Integer, primary_key=True, index=True),
        sa.Column("product_id", sa.Integer, sa.ForeignKey("products.id")),
        sa.Column("order_id", sa.Integer, sa.ForeignKey("orders.id")),
        sa.Column('created_at', sa.DateTime, default=datetime.now()),
        sa.Column('updated_at', sa.DateTime)
    )


def downgrade() -> None:
    op.drop_table("products")
    op.drop_table("orders")
    op.drop_table("order_products")
