import cv2

from insightface.app import FaceAnalysis


IMAGE_PATH = "input/test.jpg"


face_app = FaceAnalysis(
    name="buffalo_l",
    providers=["CPUExecutionProvider"]
)

face_app.prepare(
    ctx_id=-1,
    det_size=(640, 640)
)


image = cv2.imread(IMAGE_PATH)

if image is None:
    raise ValueError(
        f"Could not load image: {IMAGE_PATH}"
    )


faces = face_app.get(image)

print("Faces detected:", len(faces))

for index, face in enumerate(
    faces,
    start=1
):
    print(
        f"Face {index}: "
        f"bbox={face.bbox}, "
        f"score={face.det_score:.4f}"
    )