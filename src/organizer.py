from pathlib import Path
import shutil
import cv2

class PhotoOrganizer:

    def __init__(self, output_directory="output"):
        self.output_directory = Path(output_directory)

        self.output_directory.mkdir(
            parents=True,
            exist_ok=True
        )

    def create_person_folder(self, person_name):
        person_folder = self.output_directory / person_name

        person_folder.mkdir(
            parents=True,
            exist_ok=True
        )

        return person_folder

    def copy_photo(self, image_path, person_name):
        person_folder = self.create_person_folder(person_name)

        source = Path(image_path)
        destination = person_folder / source.name

        shutil.copy2(
            source,
            destination
        )

        return destination


    def save_main_image(
        self,
        image,
        face,
        person_name
    ):
        person_folder = self.create_person_folder(person_name)

        x1, y1, x2, y2 = face.bbox.astype(int)

        height, width = image.shape[:2]

        x1 = max(0, x1)
        y1 = max(0, y1)
        x2 = min(width, x2)
        y2 = min(height, y2)

        face_crop = image[y1:y2, x1:x2]

        main_image_path = person_folder / "main_image.jpg"

        cv2.imwrite(
            str(main_image_path),
            face_crop
        )

        return main_image_path