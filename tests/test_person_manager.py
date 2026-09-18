import cv2
from insightface.app import FaceAnalysis
from src.person_manager import PersonManager


def main():

    face_app = FaceAnalysis(
        name="buffalo_l",
        providers=["CPUExecutionProvider"]
    )

    face_app.prepare(
        ctx_id=-1,
        det_size=(640, 640)
    )

    manager = PersonManager(threshold=0.5)

    image_paths = [
        "input/p1_p1.jpg",
        "input/p1_p2.jpg",
        "input/p1_p3.jpg",
        "input/p2_p1.jpg",
        "input/p2_p2.jpg",
    ]

    for image_path in image_paths:

        print(f"\nProcessing: {image_path}")

        image = cv2.imread(image_path)

        if image is None:
            print("Could not load image.")
            continue

        faces = face_app.get(image)

        if not faces:
            print("No face detected.")
            continue

        embedding = faces[0].embedding

        person, similarity = manager.find_person(embedding)

        if person is not None:

            print(
                f"Matched: {person.name} "
                f"(similarity={similarity:.4f})"
            )

            person.add_embedding(embedding)

        else:

            person = manager.create_person(embedding)

            print(
                f"Created: {person.name} "
                f"(best similarity={similarity:.4f})"
            )

    print("\n--- People ---")

    for person in manager.people:

        print(
            f"{person.name}: "
            f"{len(person.embeddings)} embeddings"
        )


if __name__ == "__main__":
    main()