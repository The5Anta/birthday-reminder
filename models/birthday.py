from datetime import date
from models.person import Person


class Birthday:
    def __init__(self, person: Person, birth_date: date, note: str = ""):
        self.__person = person
        self.__birth_date = birth_date
        self.__note = note

    @property
    def person(self):
        return self.__person

    @property
    def birth_date(self):
        return self.__birth_date

    @property
    def note(self):
        return self.__note

    def is_today(self):
        today = date.today()
        return self.__birth_date.month == today.month and self.__birth_date.day == today.day

    def __str__(self):
        return f"{self.__person.name} - {self.__birth_date} | {self.__note}"