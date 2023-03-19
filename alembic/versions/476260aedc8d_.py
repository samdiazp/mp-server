"""empty message

Revision ID: 476260aedc8d
Revises: 
Create Date: 2023-03-07 13:01:35.441462

"""
from alembic import op
import sqlalchemy as sa
from datetime import datetime

# revision identifiers, used by Alembic.
revision = '476260aedc8d'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('email', sa.String, unique=True, index=True),
        sa.Column('role', sa.String),
        sa.Column('is_active',sa.Boolean, default=True),
        sa.Column('hashed_password', sa.String),
        sa.Column('created_at', sa.DateTime, default=datetime.now()),
        sa.Column('updated_at', sa.DateTime)
    )
    op.create_table(
        'personal_information',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String, index=True),
        sa.Column('lastname', sa.String, index=True),
        sa.Column('allergies', sa.String),
        sa.Column('pathologies', sa.String ),
        sa.Column('age',sa.Integer, nullable=False),
        sa.Column('weight', sa.Float, nullable=False),
        sa.Column('height', sa.Float, nullable=False),
        sa.Column('created_at', sa.DateTime, default=datetime.now()),
        sa.Column('updated_at', sa.DateTime),
        sa.Column('user_id',sa.Integer, sa.ForeignKey('users.id'), nullable=False),
    )


def downgrade() -> None:
    op.drop_table('users')
    op.drop_table('personal_information')
