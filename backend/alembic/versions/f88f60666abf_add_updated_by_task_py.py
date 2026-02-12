"""add_updated_by_task.py

Revision ID: f88f60666abf
Revises: 4a628681e1b7
Create Date: 2026-02-12 01:49:20.124079

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f88f60666abf'
down_revision: Union[str, Sequence[str], None] = '4a628681e1b7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    
    op.add_column(
        "tasks",
        sa.Column("updated_by", sa.Integer(), nullable=False, server_default="1"),
    )
    op.create_foreign_key(
        "fk_tasks_updated_by_users",
        "tasks",
        "users",
        ["updated_by"],
        ["id"],
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("fk_tasks_updated_by_users", "tasks", type_="foreignkey")
    op.drop_column("tasks", "updated_by")
