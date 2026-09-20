from pathlib import Path

from src.organizer import PhotoOrganizer
from src.person_repository import PersonRepository


class PersonService:

    def __init__(self, output_directory="output"):
        self.person_repository = PersonRepository()
        self.organizer = PhotoOrganizer(
            output_directory=output_directory
        )

    def load_people(self):
        return self.person_repository.load_people()

    def create_person(
        self,
        image,
        face
    ):
        # Create the database record first.
        person_data = (
            self.person_repository
            .create_person_record()
        )

        person_id = person_data["id"]
        person_name = person_data["name"]

        # Create the person's folder.
        person_folder = (
            self.organizer.create_person_folder(
                person_name
            )
        )

        # Create the main image.
        main_image_path = (
            self.organizer.save_main_image(
                image,
                face,
                person_name
            )
        )

        # Save paths in the database.
        self.person_repository.update_person_paths(
            person_id=person_id,
            folder_path=person_folder,
            main_image_path=main_image_path
        )

        return {
            "id": person_id,
            "name": person_name,
            "folder_path": str(person_folder),
            "main_image_path": str(main_image_path),
        }

    def rename_person(
        self,
        person_id,
        new_name
    ):
        people = self.load_people()

        person = next(
            (
                person
                for person in people
                if person["id"] == person_id
            ),
            None
        )

        if person is None:
            raise ValueError(
                f"Person {person_id} not found"
            )

        old_name = person["name"]

        new_name = new_name.strip()

        if not new_name:
            raise ValueError(
                "Person name cannot be empty"
            )

        if old_name == new_name:
            return person

        if self.person_repository.person_name_exists(
            new_name,
            exclude_person_id=person_id
        ):
            raise ValueError(
                f"Person name already exists: "
                f"{new_name}"
            )

        new_folder = (
            self.organizer.rename_person_folder(
                old_name,
                new_name
            )
        )

        self.person_repository.rename_person(
            person_id=person_id,
            new_name=new_name,
            new_folder_path=new_folder
        )

        return {
            "id": person_id,
            "name": new_name,
            "folder_path": str(new_folder),
            "main_image_path": str(
                Path(new_folder)
                / "main_image.jpg"
            ),
        }