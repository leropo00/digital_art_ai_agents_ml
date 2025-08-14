"""setup_vector_extension

Revision ID: bc2132d2c46d
Revises:
Create Date: 2025-08-14 21:38:17.324341

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "bc2132d2c46d"
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
