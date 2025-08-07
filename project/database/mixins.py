from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import  Mapped, mapped_column

class TimestampMixin():
    
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )
    # Automatically inserted on create
    #created_at: Mapped[datetime] = mapped_column(
    #    DateTime, nullable=False, server_default=func.now()
    #)
    # Automatically inserted on create and updated on update
    #updated_at: Mapped[datetime] = mapped_column(
    #    DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    #)
