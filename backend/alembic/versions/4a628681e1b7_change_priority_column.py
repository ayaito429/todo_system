"""change priority column

Revision ID: 4a628681e1b7
Revises: 8ee061906884
Create Date: 2026-02-09 01:37:45.505135

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4a628681e1b7'
down_revision: Union[str, Sequence[str], None] = '8ee061906884'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column(
        "tasks",
        "priority",
        existing_type=sa.Integer(),
        type_=sa.String(length=1),
        postgresql_using="priority::text"
    )


def downgrade() -> None:
    """Downgrade schema."""
    pass
