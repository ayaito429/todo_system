"""add user_id and created_by to tasks

Revision ID: fca1f48733e3
Revises: a8f924fc30df
Create Date: 2026-02-06 00:35:17.848942

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'fca1f48733e3'
down_revision: Union[str, Sequence[str], None] = 'a1b2c3d4e5f6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tasks",
        sa.Column("user_id", sa.Integer(), nullable=False),
    )
    op.add_column(
        "tasks",
        sa.Column("created_by", sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
        "fk_tasks_user_id_users",
        "tasks",
        "users",
        ["user_id"],
        ["id"],
    )
    op.create_foreign_key(
        "fk_tasks_created_by_users",
        "tasks",
        "users",
        ["created_by"],
        ["id"],
    )

def downgrade() -> None:
    op.drop_constraint("fk_tasks_created_by_users", "tasks", type_="foreignkey")
    op.drop_constraint("fk_tasks_user_id_users", "tasks", type_="foreignkey")
    op.drop_column("tasks", "created_by")
    op.drop_column("tasks", "user_id")
