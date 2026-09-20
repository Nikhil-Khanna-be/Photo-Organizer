from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import engine
from src.models import PhotoPersonModel


class PhotoPersonRepository:

    def add_person_to_photo(
        self,
        photo_id,
        person_id
    ):
        with Session(engine) as session:

            existing = session.scalars(
                select(PhotoPersonModel).where(
                    PhotoPersonModel.photo_id == photo_id,
                    PhotoPersonModel.person_id == person_id
                )
            ).first()

            if existing:
                return existing

            relationship = PhotoPersonModel(
                photo_id=photo_id,
                person_id=person_id
            )

            session.add(relationship)
            session.commit()

            return relationship