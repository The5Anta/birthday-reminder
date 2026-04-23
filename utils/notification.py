from models.birthday import Birthday


class NotificationChecker:
    def check(self, birthdays: list) -> list:
        return [b for b in birthdays if b.is_today()]

    def display(self, birthdays: list):
        todays = self.check(birthdays)
        if not todays:
            print("Šiandien gimtadienių nėra.")
        else:
            print("🎂 Šiandienos gimtadieniai:")
            for b in todays:
                print(f"  - {b}")