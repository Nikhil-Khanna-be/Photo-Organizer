import cv2
from insightface.app import FaceAnalysis
from src.face_matcher import cosine_similarity


def get_first_face_embedding(face_app, image_path):
    image = cv2.imread(image_path)

    if image is None:
        print(f"Could not load: {image_path}")
        return None

    faces = face_app.get(image)

    if not faces:
        print(f"No face found: {image_path}")
        return None

    return faces[0].embedding


def main():
    face_app = FaceAnalysis(
        name="buffalo_l",
        providers=["CPUExecutionProvider"]
    )

    face_app.prepare(
        ctx_id=-1,
        det_size=(640, 640)
    )

    images = [
        "input/p1_p1.jpg",
        "input/p1_p2.jpg",
        "input/p1_p3.jpg",
        "input/p2_p1.jpg",
        "input/p2_p2.jpg",
    ]

    embeddings = {}

    for image_path in images:
        print(f"Processing {image_path}")

        embedding = get_first_face_embedding(
            face_app,
            image_path
        )

        if embedding is not None:
            embeddings[image_path] = embedding

    print("\n--- Similarity Results ---")

    for image1, embedding1 in embeddings.items():

        for image2, embedding2 in embeddings.items():

            if image1 >= image2:
                continue

            similarity = cosine_similarity(
                embedding1,
                embedding2
            )

            print(
                f"{image1} <-> {image2}: "
                f"{similarity:.4f}"
            )


if __name__ == "__main__":
    main()