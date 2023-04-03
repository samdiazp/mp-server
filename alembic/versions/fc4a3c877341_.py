"""empty message

Revision ID: fc4a3c877341
Revises: 68209e71d9dc
Create Date: 2023-04-02 18:30:47.696705

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc4a3c877341'
down_revision = '68209e71d9dc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'sites', 
        sa.Column('id', sa.Integer, primary_key=True, index=True),                
        sa.Column('name', sa.String, nullable=False),
        sa.Column('direction', sa.String, nullable=True, default=None)
    )
   
def downgrade() -> None:
    op.drop_table('sites')
