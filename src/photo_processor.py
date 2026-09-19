import cv2
from insightface.app import FaceAnalysis
from src.organizer import PhotoOrganizer
from src.person_manager import PersonManager


class PhotoProcessor:

    def __init__(
        self,
        threshold=0.5,
        output_directory="output"
    ):
        self.face_app = FaceAnalysis(
            name="buffalo_l",
            providers=["CPUExecutionProvider"]
        )

        self.face_app.prepare(
            ctx_id=-1,
            det_size=(640, 640)
        )

        self.person_manager = PersonManager(
            threshold=threshold
        )

        self.organizer = PhotoOrganizer(
            output_directory=output_directory
        )

    def process_photo(self, image_path):

        print(f"\nProcessing: {image_path}")

        image = cv2.imread(str(image_path))

        if image is None:
            print("Could not load image.")
            return []

        faces = self.face_app.get(image)

        print(f"Faces detected: {len(faces)}")

        if not faces:
            print("No faces found.")
            return []

        matched_people = []

        for index, face in enumerate(faces, start=1):

            print(f"\nFace {index}")

            person, similarity = (
                self.person_manager.find_person(
                    face.embedding
                )
            )

            if person is None:

                person = (
                    self.person_manager.create_person(
                        face.embedding
                    )
                )

                print(
                    f"New person created: "
                    f"{person.name}"
                )

                main_image = (
                    self.organizer.save_main_image(
                        image,
                        face,
                        person.name
                    )
                )

                print(
                    f"Main image: {main_image}"
                )

            else:

                print(
                    f"Matched: {person.name}"
                )

                print(
                    f"Similarity: "
                    f"{similarity:.4f}"
                )

                person.add_embedding(
                    face.embedding
                )

            matched_people.append(person)

        # Remove duplicates.
        unique_people = {}

        for person in matched_people:
            unique_people[person.person_id] = person

        # Copy the original photo once into
        # each person's folder.
        for person in unique_people.values():

            destination = (
                self.organizer.copy_photo(
                    image_path,
                    person.name
                )
            )

            print(
                f"Copied photo to: {destination}"
            )

        return list(unique_people.values())