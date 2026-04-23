import csv
from datetime import date
from models.person import Person
from models.birthday import Birthday


class FileHandler:
    def __init__(self, filepath: str):
        self.__filepath = filepath

    def save(self, birthdays: list):
        with open(self.__filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["name", "email", "birth_date", "note"])
            for b in birthdays:
                writer.writerow([
                    b.person.name,
                    b.person.email,
                    b.birth_date.isoformat(),
                    b.note
                ])

    def load(self) -> list:
        birthdays = []
        try:
            with open(self.__filepath, "r", encoding="utf-8") as f:
                reader = csv.DictReader(f)
                for row in reader:
                    person = Person(row["name"], row["email"])
                    birth_date = date.fromisoformat(row["birth_date"])
                    birthday = Birthday(person, birth_date, row["note"])
                    birthdays.append(birthday)
        except FileNotFoundError:
            pass
        return birthdays