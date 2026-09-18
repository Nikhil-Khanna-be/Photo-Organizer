import cv2
from insightface.app import FaceAnalysis
from src.face_matcher import cosine_similarity


def main():
    app = FaceAnalysis(
        name="buffalo_l",
        providers=["CPUExecutionProvider"]
    )

    app.prepare(
        ctx_id=0,
        det_size=(640, 640)
    )

    image1 = cv2.imread("input/p1_p1.jpg")
    image2 = cv2.imread("input/p2_p1.jpg")

    if image1 is None or image2 is None:
        print("Could not load one of the images.")
        return

    faces1 = app.get(image1)
    faces2 = app.get(image2)

    if not faces1 or not faces2:
        print("Could not find a face in one of the images.")
        return

    embedding1 = faces1[0].embedding
    embedding2 = faces2[0].embedding

    similarity = cosine_similarity(
        embedding1,
        embedding2
    )

    print(f"Similarity: {similarity:.4f}")


if __name__ == "__main__":
    main()