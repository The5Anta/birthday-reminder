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

    def days_until(self) -> int:
        today = date.today()
        next_birthday = self.__birth_date.replace(year=today.year)
        if next_birthday < today:
            next_birthday = next_birthday.replace(year=today.year + 1)
        return (next_birthday - today).days

    def age(self) -> int:
        today = date.today()
        years = today.year - self.__birth_date.year
        if (today.month, today.day) < (self.__birth_date.month, self.__birth_date.day):
            years -= 1
        return years

    def __str__(self):
        return f"{self.__person.name} - {self.__birth_date} | {self.__note}"