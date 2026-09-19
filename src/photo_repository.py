from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import engine
from src.models import PhotoModel


class PhotoRepository:

    def create_photo(self, file_path):
        with Session(engine) as session:
            existing_photo = session.scalars(
                select(PhotoModel).where(
                    PhotoModel.file_path == str(file_path)
                )
            ).first()

            if existing_photo:
                return existing_photo.id

            photo = PhotoModel(
                file_path=str(file_path)
            )

            session.add(photo)
            session.commit()

            return photo.id