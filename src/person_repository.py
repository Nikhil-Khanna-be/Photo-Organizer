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
        name,
        folder_path,
        main_image_path
    ):
        with Session(engine) as session:
            person = PersonModel(
                name=name,
                folder_path=str(folder_path),
                main_image_path=str(main_image_path)
            )

            session.add(person)
            session.commit()

            return person.id

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
            face_embedding = FaceEmbeddingModel(
                person_id=person_id,
                photo_id=photo_id,
                embedding=embedding_bytes
            )

            session.add(face_embedding)
            session.commit()

            return face_embedding.id