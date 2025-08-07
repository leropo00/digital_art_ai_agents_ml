from sqlalchemy import Integer, String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from datetime import datetime


class ArtIdea(Base):
    __tablename__ = "art_idea"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[str] = mapped_column(String(30))
    nickname: Mapped[Optional[str]]

    created = Column(DateTime, default=datetime.utcnow)    
    updated = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
