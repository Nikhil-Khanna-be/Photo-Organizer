from src.photo_repository import PhotoRepository


repository = PhotoRepository()

photo_id = repository.create_photo(
    "input/p1_p1.jpg"
)

print("Photo ID:", photo_id)