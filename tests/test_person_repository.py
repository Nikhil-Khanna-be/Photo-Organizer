from src.person_repository import PersonRepository


repository = PersonRepository()

people = repository.load_people()

print("People found:", len(people))

for person in people:
    print(
        person["id"],
        person["name"],
        "embeddings:",
        len(person["embeddings"])
    )