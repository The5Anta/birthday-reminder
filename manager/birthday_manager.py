from models.birthday import Birthday


class BirthdayManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._birthdays = []
        return cls._instance

    def add_birthday(self, birthday: Birthday):
        self._birthdays.append(birthday)

    def remove_birthday(self, name: str):
        self._birthdays = [b for b in self._birthdays if b.person.name.lower() != name.lower()]

    def get_all(self):
        return self._birthdays

    def get_todays(self):
        return [b for b in self._birthdays if b.is_today()]

    def search(self, name: str):
        return [b for b in self._birthdays if name.lower() in b.person.name.lower()]

    def __str__(self):
        return f"BirthdayManager ({len(self._birthdays)} entries)"