from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    # logic is handled on python side
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.now(),
        onupdate=datetime.now(),
    )
    # logic is handled in the database
    # created_at: Mapped[datetime] = mapped_column(
    #    DateTime, nullable=False, server_default=func.now()
    # )
    # updated_at: Mapped[datetime] = mapped_column(
    #    DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    # )
