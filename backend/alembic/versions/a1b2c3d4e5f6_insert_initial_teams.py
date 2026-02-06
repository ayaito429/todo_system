"""insert initial teams

Revision ID: a1b2c3d4e5f6
Revises: 3d998a2f968e
Create Date: 2026-02-06 01:00:00.000000

"""
from typing import Sequence, Union

from alembic import op


# revision identifiers, used by Alembic.
revision: str = 'a1b2c3d4e5f6'
down_revision: Union[str, Sequence[str], None] = '3d998a2f968e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        INSERT INTO teams (id, team_name, created_at, updated_at, deleted_flag)
        VALUES
            (1, '初期チーム', NOW(), NOW(), false);
        """
    )
    # 明示的に id を入れた場合、シーケンスを進めておくと以降の INSERT で衝突しない
    op.execute("SELECT setval('teams_id_seq', (SELECT COALESCE(MAX(id), 1) FROM teams));")


def downgrade() -> None:
    op.execute("DELETE FROM teams WHERE team_name = '初期チーム';")
