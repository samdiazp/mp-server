"""empty message

Revision ID: 45a7ca37207b
Revises: 7e219fbf6963
Create Date: 2023-02-26 14:03:29.916580

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45a7ca37207b'
down_revision = '7e219fbf6963'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'personal_information',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String),
        sa.Column('lastname', sa.String),
        sa.Column('weight', sa.Float),
        sa.Column('height', sa.Float),
        sa.Column('age' ,sa.Integer),
        sa.Column('allergies' ,sa.String),
        sa.Column('pathologies', sa.String),
        sa.Column('user_id', sa.Integer, sa.ForeignKey("users.id"), nullable=False)
    )


def downgrade() -> None:
    op.drop_table('personal_information')
