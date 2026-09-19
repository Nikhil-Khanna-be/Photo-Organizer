from src.photo_processor import PhotoProcessor


def main():

    processor = PhotoProcessor(
        threshold=0.5,
        output_directory="output"
    )

    processor.process_photo(
        "input/p1_p1.jpg"
    )
    processor.process_photo(
        "input/p1_p2.jpg"
    )


if __name__ == "__main__":
    main()