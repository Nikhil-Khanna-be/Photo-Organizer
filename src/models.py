from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    LargeBinary,
    String,
)
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass

#person table
class PersonModel(Base):
    __tablename__ = "people"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False
    )

    folder_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False
    )

    main_image_path: Mapped[str | None] = mapped_column(
        String(500),
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


#photo table
class PhotoModel(Base):
    __tablename__ = "photos"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    file_path: Mapped[str] = mapped_column(
        String(500),
        nullable=False,
        unique=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    processed_at: Mapped[datetime | None] = mapped_column(
        DateTime,
        nullable=True
    )


#face embedding table
class FaceEmbeddingModel(Base):
    __tablename__ = "face_embeddings"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True
    )

    person_id: Mapped[int] = mapped_column(
        ForeignKey("people.id"),
        nullable=False
    )

    photo_id: Mapped[int] = mapped_column(
        ForeignKey("photos.id"),
        nullable=False
    )

    embedding: Mapped[bytes] = mapped_column(
        LargeBinary,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


#Table of Photo person relation
class PhotoPersonModel(Base):
    __tablename__ = "photo_people"

    photo_id: Mapped[int] = mapped_column(
        ForeignKey("photos.id"),
        primary_key=True
    )

    person_id: Mapped[int] = mapped_column(
        ForeignKey("people.id"),
        primary_key=True
    )