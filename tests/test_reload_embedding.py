import cv2
import numpy as np

from insightface.app import FaceAnalysis

from src.face_matcher import cosine_similarity
from src.person_repository import PersonRepository


IMAGE_PATH = "input/p1_p2.jpg"


# --------------------------------------------------
# 1. Load InsightFace
# --------------------------------------------------

face_app = FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"]
)

face_app.prepare(
    ctx_id=-1,
    det_size=(640, 640)
)


# --------------------------------------------------
# 2. Load the NEW photo
# --------------------------------------------------

image = cv2.imread(IMAGE_PATH)

if image is None:
    raise ValueError(
        f"Could not load image: {IMAGE_PATH}"
    )


# --------------------------------------------------
# 3. Detect the face
# --------------------------------------------------

faces = face_app.get(image)

print("Faces detected:", len(faces))

if not faces:
    raise ValueError("No faces detected.")


new_embedding = np.asarray(
    faces[0].embedding,
    dtype=np.float32
)

print(
    "New embedding shape:",
    new_embedding.shape
)


# --------------------------------------------------
# 4. Load people FROM MYSQL
# --------------------------------------------------

repository = PersonRepository()

people = repository.load_people()

print("People loaded from MySQL:", len(people))


# --------------------------------------------------
# 5. Compare against stored embeddings
# --------------------------------------------------

for person in people:

    print(
        f"\nPerson: {person['name']}"
    )

    for stored_embedding in person["embeddings"]:

        similarity = cosine_similarity(
            new_embedding,
            stored_embedding
        )

        print(
            f"Similarity: {similarity:.4f}"
        )