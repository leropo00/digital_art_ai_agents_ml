from datetime import datetime
from enum import Enum
from typing import Optional, List

from sqlalchemy import Enum as SqlEnum
from sqlalchemy import Integer, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..base import Base
from ..mixins import TimestampMixin


class IdeaType(Enum):
    # when image has no text related with its contents
    IMAGE = "image"

    # text is integral part of art image idea
    IMAGE_WITH_CAPTION = "image_with_caption"
    # text only image, like slogans on tshirts
    CAPTION_ONLY = "caption_only"


class TitleType(Enum):
    # when title is not part of image
    # the only unique name of the image
    NOMINAL = "nominal"

    # when title is also part of the image,
    # there is always one primary title for such image, else they can't exists
    PRIMARY = "primary"
    # alternative title for sich image
    ALTERNATIVE = "alternative"


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

    titles: Mapped[List["ArtTitle"]] = relationship(back_populates="art_idea")


class ArtTitle(Base, TimestampMixin):
    __tablename__ = "art_idea_title"

    id: Mapped[int] = mapped_column(primary_key=True)
    title_type: Mapped[TitleType] = mapped_column(
        SqlEnum(TitleType, name="art_title_type", native_enum=True), nullable=False
    )
    title_text: Mapped[str] = mapped_column(String)

    art_idea_id: Mapped[int] = mapped_column(ForeignKey("art_idea.id"))
    art_idea: Mapped["ArtIdea"] = relationship("ArtIdea", back_populates="titles")
