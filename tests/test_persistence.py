import cv2

from src.photo_repository import PhotoRepository
from src.person_repository import PersonRepository
from src.photo_person_repository import PhotoPersonRepository


image_path = "input/p1_p1.jpg"

image = cv2.imread(image_path)

if image is None:
    raise ValueError("Could not load image")


photo_repository = PhotoRepository()
person_repository = PersonRepository()
relationship_repository = PhotoPersonRepository()


photo_id = photo_repository.create_photo(
    image_path
)

print("Photo ID:", photo_id)


fake_embedding = [0.1] * 512

person_id = person_repository.create_person(
    name="Test_Person",
    folder_path="output/Test_Person",
    main_image_path="output/Test_Person/main_image.jpg"
)

print("Person ID:", person_id)


embedding_id = person_repository.add_embedding(
    person_id=person_id,
    photo_id=photo_id,
    embedding=fake_embedding
)

print("Embedding ID:", embedding_id)


relationship_repository.add_person_to_photo(
    photo_id=photo_id,
    person_id=person_id
)

print("Photo-person relationship created.")