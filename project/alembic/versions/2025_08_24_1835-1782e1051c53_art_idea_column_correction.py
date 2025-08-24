"""art_idea_column_correction

Revision ID: 1782e1051c53
Revises: 9a51bc4ff76b
Create Date: 2025-08-24 18:35:22.413870

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "1782e1051c53"
down_revision: Union[str, Sequence[str], None] = "9a51bc4ff76b"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "art_idea",
        sa.Column(
            "initial_idea",
            sa.String(),
            nullable=True,
        ),
    )
    op.drop_column("art_idea", "inital_idea")


def downgrade() -> None:
    """Downgrade schema."""
    op.add_column(
        "art_idea",
        sa.Column(
            "inital_idea",
            sa.String(),
            nullable=True,
        ),
    )
    op.drop_column("art_idea", "initial_idea")
