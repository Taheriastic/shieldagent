"""Add scan_type to jobs table

Revision ID: add_scan_type_001
Revises: 53b5462080f2
Create Date: 2026-01-22

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_scan_type_001'
down_revision: Union[str, None] = '53b5462080f2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Add scan_type column with default 'quick'
    op.add_column(
        'jobs',
        sa.Column('scan_type', sa.String(50), nullable=False, server_default='quick')
    )


def downgrade() -> None:
    op.drop_column('jobs', 'scan_type')
