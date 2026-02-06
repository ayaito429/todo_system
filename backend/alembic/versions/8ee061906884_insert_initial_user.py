"""insert initial user

Revision ID: 8ee061906884
Revises: fca1f48733e3
Create Date: 2026-02-06 00:53:25.637771

"""
from typing import Sequence, Union
from core.security import get_password_hash


from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8ee061906884'
down_revision: Union[str, Sequence[str], None] = 'fca1f48733e3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass

def downgrade() -> None:
    pass
