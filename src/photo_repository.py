from datetime import datetime
from pathlib import Path

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import engine
from src.models import PhotoModel


class PhotoRepository:

    def normalize_path(self, file_path):
        return Path(file_path).as_posix()

    def create_photo(self, file_path):
        normalized_path = self.normalize_path(file_path)

        with Session(engine) as session:
            existing_photo = session.scalars(
                select(PhotoModel).where(
                    PhotoModel.file_path == normalized_path
                )
            ).first()

            if existing_photo:
                return existing_photo.id

            photo = PhotoModel(
                file_path=normalized_path
            )

            session.add(photo)
            session.commit()

            return photo.id

    def is_processed(self, file_path):
        normalized_path = self.normalize_path(file_path)

        with Session(engine) as session:
            photo = session.scalars(
                select(PhotoModel).where(
                    PhotoModel.file_path == normalized_path
                )
            ).first()

            if photo is None:
                return False

            return photo.processed_at is not None

    def mark_processed(self, photo_id):
        with Session(engine) as session:
            photo = session.get(
                PhotoModel,
                photo_id
            )

            if photo is None:
                return

            photo.processed_at = datetime.utcnow()

            session.commit()