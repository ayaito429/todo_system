"""insert initial user

Revision ID: 8ee061906884
Revises: fca1f48733e3
Create Date: 2026-02-06 00:53:25.637771

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ee061906884'
down_revision: Union[str, Sequence[str], None] = 'fca1f48733e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # op.bulk_insert + sa.text("NOW()") は型適応で f405 が出ることがあるため、生 SQL で挿入
    op.execute(
        """
        INSERT INTO users (name, email, password, role, team_id, created_at, updated_at, deleted_flag)
        VALUES
            ('初期ユーザー', 'test@example.com', 'password', 'user', 1, NOW(), NOW(), false),
            ('初期管理者', 'test_admin@example.com', 'password', 'admin', 1, NOW(), NOW(), false),
            ('初期リーダー', 'test_leader@example.com', 'password', 'leader', 1, NOW(), NOW(), false);
        """
    )

def downgrade() -> None:
    op.execute("DELETE FROM users WHERE name IN ('初期ユーザー', '初期管理者', '初期リーダー');")
