"""empty message

Revision ID: 7e219fbf6963
Revises: 
Create Date: 2023-02-26 09:30:16.870309

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7e219fbf6963'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('email', sa.String, unique=True, index=True),
        sa.Column('hashed_password', sa.String),
        sa.Column('is_active', sa.Boolean, default=True),
        sa.Column('role', sa.String)
    )

def downgrade() -> None:
    op.drop_table('users')
