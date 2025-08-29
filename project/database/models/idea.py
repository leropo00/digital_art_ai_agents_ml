from datetime import datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, String
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
    idea_type: Mapped[IdeaType] = mapped_column(
        SqlEnum(IdeaType, name="art_idea_type", native_enum=True), nullable=False
    )

    slug: Mapped[str] = mapped_column(String, unique=True)
    initial_idea: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    # this field will be used to convert to vectore embeddings
    final_description: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    titles: Mapped[List["ArtIdeaTitle"]] = relationship(
        back_populates="art_idea",
        cascade="all, delete",
    )
    questions: Mapped[List["ArtIdeaQuestion"]] = relationship(
        back_populates="art_idea",
        cascade="all, delete",
    )
    reference_material: Mapped[List["ReferenceMaterial"]] = relationship(
        secondary="art_idea_references",
        back_populates="art_ideas",
    )


class ArtIdeaTitle(Base, TimestampMixin):
    __tablename__ = "art_idea_title"

    id: Mapped[int] = mapped_column(primary_key=True)
    title_text: Mapped[str] = mapped_column(String)
    title_type: Mapped[TitleType] = mapped_column(
        SqlEnum(TitleType, name="art_title_type", native_enum=True), nullable=False
    )

    art_idea_id: Mapped[int] = mapped_column(ForeignKey("art_idea.id"))
    art_idea: Mapped["ArtIdea"] = relationship("ArtIdea", back_populates="titles")


class ArtIdeaQuestion(Base, TimestampMixin):
    __tablename__ = "art_idea_question"

    id: Mapped[int] = mapped_column(primary_key=True)

    question_text: Mapped[str] = mapped_column(String)
    solved_date: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=True,
    )

    art_idea_id: Mapped[int] = mapped_column(ForeignKey("art_idea.id"))
    art_idea: Mapped["ArtIdea"] = relationship("ArtIdea", back_populates="questions")


class ArtIdeaReferences(Base, TimestampMixin):
    __tablename__ = "art_idea_references"

    id: Mapped[int] = mapped_column(primary_key=True)
    art_idea_id: Mapped[int] = mapped_column(ForeignKey("art_idea.id"))
    reference_material_id: Mapped[int] = mapped_column(
        ForeignKey("reference_material.id")
    )

    reference_usage: Mapped[Optional[str]] = mapped_column(String, nullable=True)


# import at bottom as workaround against circular dependencies
from .reference import ReferenceMaterial
