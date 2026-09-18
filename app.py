import cv2
from src.face_detector import create_face_detector
from src.face_matcher import cosine_similarity

def main():
    image_path = "input/test.jpg"

    image = cv2.imread(image_path)

    if image is None:
        print("Could not load image.")
        return

    print("Image loaded successfully!")

    height, width, channels = image.shape

    print(f"Width: {width}")
    print(f"Height: {height}")
    print(f"Channels: {channels}")
    print(f"Total pixels: {width * height}")

    face_app=create_face_detector()
    faces=face_app.get(image)

    print(f"Faces detected: {len(faces)}")

    if len(faces) >= 2:
        embedding1 = faces[0].embedding
        embedding2 = faces[1].embedding
        similarity = cosine_similarity(
            embedding1,
            embedding2
        )
        print(f"Similarity between Face 1 and Face 2: {similarity:.4f}")

    for i, face in enumerate(faces, start=1):
        print(f"\nFace {i}")
        print(f"Bounding box: {face.bbox}")
        print(f"Detection score: {face.det_score}")
        print(f"Embedding shape: {face.embedding.shape}")
        print(f"First 10 values: {face.embedding[:10]}")


    for face in faces:
        x1, y1, x2, y2 = face.bbox.astype(int)
        cv2.rectangle(
            image,
            (x1, y1),
            (x2, y2),
            (0, 255, 0),
            2
        )

    cv2.imwrite("output/detected.jpg", image)
    print("Saved result to output/detected.jpg")


if __name__ == "__main__":
    main()