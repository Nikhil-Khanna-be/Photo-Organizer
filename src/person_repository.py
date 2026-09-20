import numpy as np

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import engine
from src.models import (
    FaceEmbeddingModel,
    PersonModel,
)


class PersonRepository:

    def load_people(self):
        people = []

        with Session(engine) as session:
            person_rows = session.scalars(
                select(PersonModel)
            ).all()

            for person_row in person_rows:
                embeddings = []

                embedding_rows = session.scalars(
                    select(FaceEmbeddingModel).where(
                        FaceEmbeddingModel.person_id
                        == person_row.id
                    )
                ).all()

                for embedding_row in embedding_rows:
                    embedding = np.frombuffer(
                        embedding_row.embedding,
                        dtype=np.float32
                    )

                    embeddings.append(embedding)

                people.append(
                    {
                        "id": person_row.id,
                        "name": person_row.name,
                        "folder_path": person_row.folder_path,
                        "main_image_path": (
                            person_row.main_image_path
                        ),
                        "embeddings": embeddings,
                    }
                )

        return people

    def create_person(
        self,
        folder_path,
        main_image_path
    ):
        with Session(engine) as session:
            person = PersonModel(
                name="TEMP",
                folder_path=str(folder_path),
                main_image_path=str(main_image_path)
            )

            session.add(person)
            session.flush()

            person.name = (
                f"Person_{person.id:03d}"
            )

            session.commit()

            return {
                "id": person.id,
                "name": person.name
            }

        
    def add_embedding(
        self,
        person_id,
        photo_id,
        embedding
    ):
        embedding_bytes = (
            np.asarray(
                embedding,
                dtype=np.float32
            ).tobytes()
        )

        with Session(engine) as session:

            existing = session.scalars(
                select(FaceEmbeddingModel).where(
                    FaceEmbeddingModel.person_id == person_id,
                    FaceEmbeddingModel.photo_id == photo_id
                )
            ).first()

            if existing:
                return existing.id

            face_embedding = FaceEmbeddingModel(
                person_id=person_id,
                photo_id=photo_id,
                embedding=embedding_bytes
            )

            session.add(face_embedding)
            session.commit()

            return face_embedding.id


    def create_person_record(self):
        with Session(engine) as session:
            person = PersonModel(
                name="TEMP",
                folder_path="",
                main_image_path=None
            )

            session.add(person)
            session.flush()

            person.name = (
                f"Person_{person.id:03d}"
            )

            session.commit()

            return {
                "id": person.id,
                "name": person.name
            }

    def update_person_paths(
        self,
        person_id,
        folder_path,
        main_image_path
    ):
        with Session(engine) as session:
            person = session.get(
                PersonModel,
                person_id
            )

            if person is None:
                raise ValueError(
                    f"Person {person_id} not found"
                )

            person.folder_path = str(
                folder_path
            )

            person.main_image_path = str(
                main_image_path
            )

            session.commit()


    def rename_person(
        self,
        person_id,
        new_name,
        new_folder_path
    ):
        with Session(engine) as session:
            person = session.get(
                PersonModel,
                person_id
            )

            if person is None:
                raise ValueError(
                    f"Person {person_id} not found"
                )

            existing_person = session.scalars(
                select(PersonModel).where(
                    PersonModel.name == new_name,
                    PersonModel.id != person_id
                )
            ).first()

            if existing_person:
                raise ValueError(
                    f"Person name already exists: "
                    f"{new_name}"
                )

            person.name = new_name
            person.folder_path = str(
                new_folder_path
            )

            session.commit()

    def person_name_exists(
        self,
        name,
        exclude_person_id=None
    ):
        with Session(engine) as session:
            query = select(PersonModel).where(
                PersonModel.name == name
            )

            if exclude_person_id is not None:
                query = query.where(
                    PersonModel.id != exclude_person_id
                )

            return session.scalars(query).first() is not None