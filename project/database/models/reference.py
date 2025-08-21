from enum import Enum
from typing import List

from sqlalchemy import DateTime, Enum as SqlEnum, ForeignKey, String
from sqlalchemy.orm import relationship, Mapped, mapped_column

from ..base import Base
from ..mixins import TimestampMixin


class ReferenceMaterialType(Enum):
    IMAGE = "image"
    TUTORIAL_VIDEO = "tutorial_video"
    TUTORIAL_ARTICLE = "tutorial_article"
    PROMPT = "prompt"


class StorageType(Enum):
    LOCAL_DISK = "local_disk"
    URL_LINK = "url_link"


class ReferenceMaterial(Base, TimestampMixin):
    __tablename__ = "reference_material"

    id: Mapped[int] = mapped_column(primary_key=True)
    idea_type: Mapped[ReferenceMaterialType] = mapped_column(
        SqlEnum(
            ReferenceMaterialType,
            name="reference_material_type_enum",
            native_enum=True,
        ),
        nullable=False,
    )

    description: Mapped[str] = mapped_column(String)

    storage: Mapped[List["ReferenceStorage"]] = relationship(
        back_populates="reference_material",
        cascade="all, delete",
    )
    art_ideas: Mapped[List["ArtIdea"]] = relationship(
        secondary="art_idea_references",
        back_populates="reference_material",
    )


class ReferenceStorage(Base, TimestampMixin):
    __tablename__ = "reference_storage"

    id: Mapped[int] = mapped_column(primary_key=True)
    storage_type: Mapped[StorageType] = mapped_column(
        SqlEnum(StorageType, name="storage_type_enum", native_enum=True),
        nullable=False,
    )

    storage_link: Mapped[str] = mapped_column(String)

    reference_material_id: Mapped[int] = mapped_column(
        ForeignKey("reference_material.id")
    )
    reference_material: Mapped["ReferenceMaterial"] = relationship(
        "ReferenceMaterial", back_populates="storage"
    )


# import at bottom as workaround against circular dependencies
from .idea import ArtIdea
