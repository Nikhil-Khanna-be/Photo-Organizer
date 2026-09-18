from src.face_matcher import cosine_similarity
from src.person import Person


class PersonManager:

    def __init__(self, threshold=0.5):
        self.people = []
        self.threshold = threshold

    def find_person(self, embedding):

        best_person = None
        best_similarity = -1.0

        for person in self.people:

            for known_embedding in person.embeddings:

                similarity = cosine_similarity(
                    embedding,
                    known_embedding
                )

                if similarity > best_similarity:
                    best_similarity = similarity
                    best_person = person

        if best_similarity >= self.threshold:
            return best_person, best_similarity

        return None, best_similarity

    def create_person(self, embedding):

        person_id = len(self.people) + 1

        name = f"Person_{person_id:03d}"

        person = Person(
            person_id=person_id,
            name=name,
            embedding=embedding
        )

        self.people.append(person)

        return person