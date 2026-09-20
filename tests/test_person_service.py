from src.person_service import PersonService


def main():
    service = PersonService("output")

    people = service.load_people()

    print(f"People loaded: {len(people)}")

    for person in people:
        print(
            f"{person['id']}: "
            f"{person['name']}"
        )


if __name__ == "__main__":
    main()