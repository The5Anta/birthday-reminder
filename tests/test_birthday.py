import unittest
from datetime import date
from models.person import Person
from models.birthday import Birthday
from manager.birthday_manager import BirthdayManager


class TestPerson(unittest.TestCase):

    def test_person_name(self):
        person = Person("Jonas", "jonas@gmail.com")
        self.assertEqual(person.name, "Jonas")

    def test_person_email(self):
        person = Person("Jonas", "jonas@gmail.com")
        self.assertEqual(person.email, "jonas@gmail.com")

    def test_person_str(self):
        person = Person("Jonas", "jonas@gmail.com")
        self.assertEqual(str(person), "Jonas (jonas@gmail.com)")

    def test_user_str(self):
        from models.person import User
        user = User("Jonas", "jonas@gmail.com")
        self.assertEqual(str(user), "User: Jonas")

    def test_user_inherits_person(self):
        from models.person import User
        user = User("Jonas", "jonas@gmail.com")
        self.assertIsInstance(user, Person)


class TestBirthday(unittest.TestCase):

    def setUp(self):
        self.person = Person("Jonas", "jonas@gmail.com")
        self.birthday = Birthday(self.person, date(1990, 4, 23), "draugas")

    def test_birthday_person(self):
        self.assertEqual(self.birthday.person.name, "Jonas")

    def test_birthday_date(self):
        self.assertEqual(self.birthday.birth_date, date(1990, 4, 23))

    def test_birthday_note(self):
        self.assertEqual(self.birthday.note, "draugas")

    def test_birthday_str(self):
        self.assertIn("Jonas", str(self.birthday))

    def test_is_today_false(self):
        birthday = Birthday(self.person, date(1990, 1, 1))
        self.assertFalse(birthday.is_today())

    def test_age(self):
        today = date.today()
        birth = date(today.year - 25, today.month, today.day)
        birthday = Birthday(self.person, birth)
        self.assertEqual(birthday.age(), 25)

    def test_age_before_birthday(self):
        today = date.today()
        birth = date(today.year - 25, today.month, today.day + 1) if today.day < 28 else date(today.year - 25, today.month, 1)
        birthday = Birthday(self.person, birth)
        self.assertEqual(birthday.age(), 24)

    def test_days_until_today(self):
        today = date.today()
        birthday = Birthday(self.person, date(1990, today.month, today.day))
        self.assertEqual(birthday.days_until(), 0)

    def test_days_until_positive(self):
        self.assertGreaterEqual(self.birthday.days_until(), 0)


class TestBirthdayManager(unittest.TestCase):

    def setUp(self):
        BirthdayManager._instance = None
        self.manager = BirthdayManager()
        self.person = Person("Ana", "ana@gmail.com")
        self.birthday = Birthday(self.person, date(1995, 6, 15))

    def test_add_birthday(self):
        self.manager.add_birthday(self.birthday)
        self.assertEqual(len(self.manager.get_all()), 1)

    def test_remove_birthday(self):
        self.manager.add_birthday(self.birthday)
        self.manager.remove_birthday("Ana")
        self.assertEqual(len(self.manager.get_all()), 0)

    def test_search_found(self):
        self.manager.add_birthday(self.birthday)
        results = self.manager.search("Ana")
        self.assertEqual(len(results), 1)

    def test_search_not_found(self):
        self.manager.add_birthday(self.birthday)
        results = self.manager.search("Petras")
        self.assertEqual(len(results), 0)

    def test_singleton(self):
        manager2 = BirthdayManager()
        self.assertIs(self.manager, manager2)

    def test_get_all_empty(self):
        self.assertEqual(self.manager.get_all(), [])

    def test_no_duplicates(self):
        self.manager.add_birthday(self.birthday)
        self.manager.add_birthday(self.birthday)
        self.assertEqual(len(self.manager.get_all()), 1)

    def test_get_todays(self):
        today = date.today()
        birthday_today = Birthday(self.person, date(1990, today.month, today.day))
        self.manager.add_birthday(birthday_today)
        self.assertEqual(len(self.manager.get_todays()), 1)


if __name__ == "__main__":
    unittest.main()