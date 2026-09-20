from pathlib import Path
import cv2
import numpy as np

from insightface.app import FaceAnalysis

from src.face_matcher import cosine_similarity
from src.organizer import PhotoOrganizer
from src.person_repository import PersonRepository
from src.photo_person_repository import PhotoPersonRepository
from src.photo_repository import PhotoRepository



class PhotoProcessor:

    def __init__(
        self,
        threshold=0.5,
        output_directory="output"
    ):
        self.threshold = threshold

        self.face_app = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"]
        )

        self.face_app.prepare(
            ctx_id=-1,
            det_size=(640, 640)
        )

        self.person_repository = PersonRepository()
        self.photo_repository = PhotoRepository()
        self.photo_person_repository = (
            PhotoPersonRepository()
        )

        self.organizer = PhotoOrganizer(
            output_directory=output_directory
        )

    def find_person(self, embedding, people):
        best_person = None
        best_similarity = -1.0

        for person in people:

            for known_embedding in person["embeddings"]:

                similarity = cosine_similarity(
                    embedding,
                    known_embedding
                )

                if similarity > best_similarity:
                    best_similarity = similarity
                    best_person = person

        if best_similarity >= self.threshold:
            return best_person, best_similarity

        return None, best_similarity

    def process_photo(self, image_path):

        print(f"\nProcessing: {image_path}")
        if self.photo_repository.is_processed(
            image_path
        ):
            print(
                f"Already processed: {image_path}"
            )
            return []

        # ------------------------------------------
        # 1. Load image
        # ------------------------------------------

        image = cv2.imread(str(image_path))

        if image is None:
            print("Could not load image.")
            return []

        # ------------------------------------------
        # 2. Detect faces
        # ------------------------------------------

        faces = self.face_app.get(image)

        print(
            f"Faces detected: {len(faces)}"
        )

        if not faces:
            print("No faces found.")
            return []

        # ------------------------------------------
        # 3. Create/find photo record
        # ------------------------------------------

        photo_id = (
            self.photo_repository.create_photo(
                image_path
            )
        )

        print(
            f"Photo ID: {photo_id}"
        )

        # ------------------------------------------
        # 4. Load existing people from MySQL
        # ------------------------------------------

        people = (
            self.person_repository.load_people()
        )

        print(
            f"People loaded: {len(people)}"
        )

        matched_people = []

        # ------------------------------------------
        # 5. Process every detected face
        # ------------------------------------------

        for index, face in enumerate(
            faces,
            start=1
        ):

            print(f"\nFace {index}")

            embedding = np.asarray(
                face.embedding,
                dtype=np.float32
            )

            # --------------------------------------
            # Try to find existing person
            # --------------------------------------

            person, similarity = self.find_person(
                embedding,
                people
            )

            # --------------------------------------
            # Existing person
            # --------------------------------------

            if person is not None:

                print(
                    f"Matched: {person['name']}"
                )

                print(
                    f"Similarity: "
                    f"{similarity:.4f}"
                )

                person_id = person["id"]

                # Save this new embedding too.
                self.person_repository.add_embedding(
                    person_id=person_id,
                    photo_id=photo_id,
                    embedding=embedding
                )

                # Keep our in-memory list updated
                # in case another face in this same
                # photo needs it.
                person["embeddings"].append(
                    embedding
                )

            # --------------------------------------
            # New person
            # --------------------------------------

            else:

                next_number = len(people) + 1

                person_name = (
                    f"Person_{next_number:03d}"
                )

                person_folder = (
                    self.organizer.create_person_folder(
                        person_name
                    )
                )

                main_image_path = (
                    self.organizer.save_main_image(
                        image,
                        face,
                        person_name
                    )
                )

                person_id = (
                    self.person_repository.create_person(
                        name=person_name,
                        folder_path=person_folder,
                        main_image_path=main_image_path
                    )
                )

                self.person_repository.add_embedding(
                    person_id=person_id,
                    photo_id=photo_id,
                    embedding=embedding
                )

                person = {
                    "id": person_id,
                    "name": person_name,
                    "folder_path": str(
                        person_folder
                    ),
                    "main_image_path": str(
                        main_image_path
                    ),
                    "embeddings": [embedding]
                }

                people.append(person)

                print(
                    f"New person created: "
                    f"{person_name}"
                )

                print(
                    f"Main image: "
                    f"{main_image_path}"
                )

            # --------------------------------------
            # Connect photo ↔ person
            # --------------------------------------

            self.photo_person_repository.add_person_to_photo(
                photo_id=photo_id,
                person_id=person_id
            )

            matched_people.append(person)

        # ------------------------------------------
        # 6. Copy photo into person folders
        # ------------------------------------------

        unique_people = {}

        for person in matched_people:
            unique_people[person["id"]] = person

        for person in unique_people.values():

            destination, copied = (
                self.organizer.copy_photo(
                    image_path,
                    person["name"]
                )
            )

            if copied:
                print(
                    f"Copied photo to: {destination}"
                )
            else:
                print(
                    f"Already exists: {destination}"
                )
        self.photo_repository.mark_processed(
            photo_id
        )

        return list(
            unique_people.values()
        )


    def process_directory(self, directory):
        directory = Path(directory)

        if not directory.exists():
            raise ValueError(
                f"Directory does not exist: {directory}"
            )

        if not directory.is_dir():
            raise ValueError(
                f"Not a directory: {directory}"
            )

        image_extensions = {
            ".jpg",
            ".jpeg",
            ".png",
            ".bmp",
            ".webp"
        }

        image_paths = sorted(
            path
            for path in directory.iterdir()
            if path.is_file()
            and path.suffix.lower()
            in image_extensions
        )

        print(
            f"\nFound {len(image_paths)} image(s)."
        )

        for image_path in image_paths:

            if self.photo_repository.is_processed(
                image_path
            ):
                print(
                    f"\nSkipping already processed: "
                    f"{image_path}"
                )
                continue

            photo_id = self.photo_repository.create_photo(
                image_path
            )

            self.process_photo(image_path)

            self.photo_repository.mark_processed(
                photo_id
            )

            print(
                f"Finished: {image_path}"
            )