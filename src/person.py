class Person:
    def __init__(self, person_id, name, embedding):
        self.person_id = person_id
        self.name = name
        self.embeddings = [embedding]

    def add_embedding(self, embedding):
        self.embeddings.append(embedding)