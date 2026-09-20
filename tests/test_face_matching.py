import numpy as np

from src.face_matcher import cosine_similarity
from src.person_repository import PersonRepository


def main():
    repository = PersonRepository()
    people = repository.load_people()

    print(f"People loaded: {len(people)}")

    for person in people:
        embeddings = person["embeddings"]

        print(
            f"\n{person['name']}: "
            f"{len(embeddings)} embedding(s)"
        )

        # Compare different photos of the same person.
        if len(embeddings) >= 2:
            for i in range(len(embeddings)):
                for j in range(i + 1, len(embeddings)):
                    similarity = cosine_similarity(
                        embeddings[i],
                        embeddings[j]
                    )

                    print(
                        f"  same person "
                        f"embedding {i + 1} ↔ "
                        f"embedding {j + 1}: "
                        f"{similarity:.4f}"
                    )

    # Compare the first embedding of every
    # different person.
    print("\nDifferent-person comparisons:")

    for i in range(len(people)):
        for j in range(i + 1, len(people)):
            embedding1 = people[i]["embeddings"][0]
            embedding2 = people[j]["embeddings"][0]

            similarity = cosine_similarity(
                embedding1,
                embedding2
            )

            print(
                f"  {people[i]['name']} ↔ "
                f"{people[j]['name']}: "
                f"{similarity:.4f}"
            )


if __name__ == "__main__":
    main()