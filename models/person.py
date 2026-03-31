class Person:
    def __init__(self, name: str, email: str):
        self.__name = name
        self.__email = email

    @property
    def name(self):
        return self.__name

    @property
    def email(self):
        return self.__email

    def __str__(self):
        return f"{self.__name} ({self.__email})"


class User(Person):
    def __init__(self, name: str, email: str):
        super().__init__(name, email)

    def __str__(self):
        return f"User: {self.name}"