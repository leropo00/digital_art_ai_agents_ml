from datetime import datetime
from sqlalchemy import DateTime, func
from sqlalchemy.orm import  Mapped, mapped_column

class TimestampMixin():
    # logic is handled on python side    
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
    )
    # logic is handled in the database
    #created_at: Mapped[datetime] = mapped_column(
    #    DateTime, nullable=False, server_default=func.now()
    #)
    #updated_at: Mapped[datetime] = mapped_column(
    #    DateTime, nullable=False, server_default=func.now(), onupdate=func.now()
    #)
