from datetime import datetime
from enum import Enum
from typing import Optional

from fastapi import HTTPException
from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from ..base import Base
from ..mixins import TimestampMixin


class IdeaType(Enum):
    # painting like, only image is important
    IMAGE = "image"
    # caption is also part of an image, for tshirt with images
    IMAGE_WITH_CAPTION = "image_with_caption"
    CAPTION_ONLY = "caption_only"


class ArtIdea(Base, TimestampMixin):
    __tablename__ = "art_idea"

    id: Mapped[int] = mapped_column(primary_key=True)
    identifier_name: Mapped[str] = mapped_column(String, unique=True)
    slug: Mapped[str] = mapped_column(String, unique=True)

    idea_type: Mapped[IdeaType] = mapped_column(
        SqlEnum(IdeaType, name="idea_type", native_enum=True), nullable=False
    )

    inital_idea: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # this field will be used to comvert to vectore embeddings
    final_description: Mapped[Optional[str]] = mapped_column(String, nullable=True)
