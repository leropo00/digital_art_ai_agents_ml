from datetime import datetime
from datetime import timezone

from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    # logic is handled on python side
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc)
    )
    # logic is handled in the database
    # created_at: Mapped[datetime] = mapped_column(
    #    DateTime, nullable=False, server_default=func.now()
    # )
    # updated_at: Mapped[datetime] = mapped_column(
    #    DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    # )
