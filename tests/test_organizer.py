import cv2
from insightface.app import FaceAnalysis
from src.organizer import PhotoOrganizer


def main():

    image_path = "input/p1_p1.jpg"

    image = cv2.imread(image_path)

    if image is None:
        print("Could not load image.")
        return

    face_app = FaceAnalysis(
        name="buffalo_l",
        providers=["CPUExecutionProvider"]
    )

    face_app.prepare(
        ctx_id=-1,
        det_size=(640, 640)
    )

    faces = face_app.get(image)

    if not faces:
        print("No face detected.")
        return

    organizer = PhotoOrganizer()

    person_name = "Test_Person"

    main_image = organizer.save_main_image(
        image,
        faces[0],
        person_name
    )

    print(
        f"Main image saved to: {main_image}"
    )


if __name__ == "__main__":
    main()