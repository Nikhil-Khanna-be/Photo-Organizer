from src.photo_processor import PhotoProcessor


def main():

    processor = PhotoProcessor(
        threshold=0.5,
        output_directory="output"
    )

    processor.process_directory(
        "input"
    )


if __name__ == "__main__":
    main()