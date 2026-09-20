import cv2
import numpy as np

from insightface.app import FaceAnalysis

from src.photo_repository import PhotoRepository
from src.person_repository import PersonRepository
from src.photo_person_repository import PhotoPersonRepository


IMAGE_PATH = "input/p1_p1.jpg"


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
# 2. Load image
# --------------------------------------------------

image = cv2.imread(IMAGE_PATH)

if image is None:
    raise ValueError(
        f"Could not load image: {IMAGE_PATH}"
    )


# --------------------------------------------------
# 3. Detect faces
# --------------------------------------------------

faces = face_app.get(image)

print("Faces detected:", len(faces))

if not faces:
    raise ValueError("No faces detected.")


# --------------------------------------------------
# 4. Get the first face embedding
# --------------------------------------------------

face = faces[0]

embedding = np.asarray(
    face.embedding,
    dtype=np.float32
)

print("Embedding shape:", embedding.shape)


# --------------------------------------------------
# 5. Create/find photo
# --------------------------------------------------

photo_repository = PhotoRepository()

photo_id = photo_repository.create_photo(
    IMAGE_PATH
)

print("Photo ID:", photo_id)


# --------------------------------------------------
# 6. Create person
# --------------------------------------------------

person_repository = PersonRepository()

person_id = person_repository.create_person(
    name="Person_001",
    folder_path="output/Person_001",
    main_image_path="output/Person_001/main_image.jpg"
)

print("Person ID:", person_id)


# --------------------------------------------------
# 7. Save real embedding
# --------------------------------------------------

embedding_id = person_repository.add_embedding(
    person_id=person_id,
    photo_id=photo_id,
    embedding=embedding
)

print("Embedding ID:", embedding_id)


# --------------------------------------------------
# 8. Create photo-person relationship
# --------------------------------------------------

relationship_repository = PhotoPersonRepository()

relationship_repository.add_person_to_photo(
    photo_id=photo_id,
    person_id=person_id
)

print("Photo-person relationship created.")