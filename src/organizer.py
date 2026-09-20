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

        if destination.exists():
            return destination, False

        shutil.copy2(source, destination)

        return destination, True


    def save_main_image(self, image, face, person_name):
        person_folder = self.create_person_folder(
            person_name
        )

        main_image_path = person_folder / "main_image.jpg"

        if main_image_path.exists():
            return main_image_path

        x1, y1, x2, y2 = face.bbox.astype(int)

        height, width = image.shape[:2]

        # Face center
        center_x = (x1 + x2) // 2
        center_y = (y1 + y2) // 2

        # Face size
        face_width = x2 - x1
        face_height = y2 - y1

        # Make the crop larger than the face.
        crop_size = int(
            max(face_width, face_height) * 2.0
        )

        half_size = crop_size // 2

        crop_x1 = center_x - half_size
        crop_y1 = center_y - half_size
        crop_x2 = center_x + half_size
        crop_y2 = center_y + half_size

        # Keep crop inside image boundaries.
        crop_x1 = max(0, crop_x1)
        crop_y1 = max(0, crop_y1)
        crop_x2 = min(width, crop_x2)
        crop_y2 = min(height, crop_y2)

        face_crop = image[
            crop_y1:crop_y2,
            crop_x1:crop_x2
        ]

        if face_crop.size == 0:
            raise ValueError(
                f"Could not crop face for {person_name}"
            )

        # Resize to a consistent size.
        main_image = cv2.resize(
            face_crop,
            (512, 512),
            interpolation=cv2.INTER_CUBIC
        )

        cv2.imwrite(
            str(main_image_path),
            main_image
        )

        return main_image_path

    def rename_person_folder(
        self,
        old_name,
        new_name
    ):
        old_folder = (
            self.output_directory / old_name
        )

        new_folder = (
            self.output_directory / new_name
        )

        if not old_folder.exists():
            raise ValueError(
                f"Person folder does not exist: "
                f"{old_folder}"
            )

        if new_folder.exists():
            raise ValueError(
                f"Destination folder already exists: "
                f"{new_folder}"
            )

        old_folder.rename(new_folder)

        return new_folder