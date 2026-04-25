# Birthday Reminder – Kursinio darbo ataskaita

## 1. Įvadas

### Kas yra ši programa?
Birthday Reminder – tai Python programavimo kalba sukurta gimtadienių priminimo programa su grafine vartotojo sąsaja (tkinter). Programa leidžia vartotojui pridėti, redaguoti, ištrinti ir ieškoti gimtadienių. Paleidus programą automatiškai pranešama apie šiandieninius gimtadienius ir artėjančius per nustatytą dienų skaičių.

### Kaip paleisti programą?
1. Įsitikink kad įdiegtas Python 3.10 ar naujesnė versija
2. Atsisiųsk arba klonuok repozitoriją iš GitHub:
```
   git clone https://github.com/The5Anta/birthday-reminder
```
3. Įdiek reikalingas bibliotekas:
```
   pip install -r requirements.txt
```
4. Paleisk `main.py` failą:
```
   python main.py
```

### Kaip naudotis programa?
- **Pridėti gimtadienį** – užpildyk formos laukelius (vardas, el. paštas, gimimo data, pastaba, priminti likus dienų) ir spausk „Išsaugoti"
- **Redaguoti** – pasirink įrašą sąraše ir spausk „Redaguoti", pakeisk duomenis ir spausk „Atnaujinti"
- **Ištrinti** – pasirink įrašą sąraše ir spausk „Ištrinti"
- **Paieška** – rašyk vardą paieškos laukelyje, sąrašas filtruojamas realiu laiku
- **Kalendorius** – pereik į „Kalendorius" tab'ą, gimtadienių dienos pažymėtos raudonai, spustelėjus ant dienos rodoma informacija apie gimtadienį
- **Eksportuoti** – spausk „Eksportuoti CSV" ir pasirink kur išsaugoti failą
- **Importuoti** – spausk „Importuoti CSV" ir pasirink failą (turi būti UTF-8 formato)
- **Gimtadienio pranešimas** – paleidus programą automatiškai rodomas pranešimas jei šiandien yra kažkieno gimtadienis

---

## 2. Analizė

### 4 OOP pilieriai

#### Inkapsuliacija (Encapsulation)
Inkapsuliacija – tai duomenų slėpimas klasės viduje. Laukai yra privatūs ir pasiekiami tik per `@property` metodus, tai apsaugo duomenis nuo netyčinio pakeitimo iš išorės.

```python
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
```

`self.__name` ir `self.__email` yra privatūs laukai – prie jų negalima prieiti tiesiogiai iš išorės. Tai užtikrina kad duomenys keičiami tik per kontroliuojamus metodus.

#### Paveldimumas (Inheritance)
Paveldimumas leidžia vienai klasei perimti kitos klasės savybes ir metodus, taip išvengiant kodo dubliavimo.

```python
class User(Person):
    def __init__(self, name: str, email: str):
        super().__init__(name, email)

    def __str__(self):
        return f"User: {self.name}"
```

`User` klasė paveldi iš `Person` – gauna visus `Person` laukus ir metodus, bet gali juos perrašyti. `super().__init__()` iškviečia tėvinės klasės konstruktorių.

#### Polimorfizmas (Polymorphism)
Polimorfizmas leidžia skirtingoms klasėms turėti tą patį metodo pavadinimą su skirtinga elgsena.

```python
# Person klasėje:
def __str__(self):
    return f"{self.__name} ({self.__email})"

# User klasėje:
def __str__(self):
    return f"User: {self.name}"
```

Abu `__str__` metodai turi tą patį pavadinimą, tačiau grąžina skirtingą rezultatą priklausomai nuo objekto tipo. Python automatiškai iškviečia tinkamą metodą.

#### Abstrakcija (Abstraction)
Abstrakcija slepia sudėtingą implementaciją ir pateikia paprastą sąsają.

```python
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
```

Vartotojas tiesiog iškviečia `display()` – jam nereikia žinoti kaip tikrinama data ar kaip filtruojamas sąrašas. Sudėtinga logika paslėpta klasės viduje.

---

### Design Pattern – Singleton

Singleton užtikrina kad per visą programą egzistuoja tik vienas klasės objektas.

```python
class BirthdayManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._birthdays = []
        return cls._instance
```

`BirthdayManager` naudoja Singleton pattern nes neturi prasmės turėti du atskirus gimtadienių sąrašus toje pačioje programoje. Kiekvieną kartą iškvietus `BirthdayManager()` grąžinamas tas pats objektas su tais pačiais duomenimis. Tai patvirtina unit testas:

```python
def test_singleton(self):
    manager2 = BirthdayManager()
    self.assertIs(self.manager, manager2)
```

---

### Kompozicija ir agregacija (Composition & Aggregation)

**Agregacija** – `Birthday` klasė naudoja `Person` objektą, bet jo nekuria ir nenaikina:

```python
class Birthday:
    def __init__(self, person: Person, birth_date: date, note: str = ""):
        self.__person = person
        self.__birth_date = birth_date
        self.__note = note
```

`Person` objektas egzistuoja nepriklausomai nuo `Birthday` – tai agregacija. Galima turėti `Person` be `Birthday`.

**Kompozicija** – `BirthdayManager` valdo gimtadienių sąrašą kuris priklauso tik jam:

```python
cls._instance._birthdays = []
```

Sunaikinus `BirthdayManager` – sunaikinamas ir visas gimtadienių sąrašas. Sąrašas negali egzistuoti be `BirthdayManager`.

---

### Papildomi Birthday klasės metodai

`Birthday` klasė turi du papildomus metodus kurie praturtina programos funkcionalumą:

```python
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
```

`days_until()` apskaičiuoja kiek dienų liko iki artėjančio gimtadienio, `age()` apskaičiuoja dabartinį amžių tiksliai atsižvelgiant į tai ar gimtadienis jau buvo šiemet.

---

### Failų skaitymas ir rašymas

Programa naudoja CSV formatą duomenims išsaugoti. `FileHandler` klasė atsakinga už visas failo operacijas:

```python
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
```

Duomenys automatiškai išsaugomi po kiekvieno pakeitimo ir užkraunami paleidžiant programą. Vartotojas taip pat gali eksportuoti duomenis į pasirinktą vietą arba importuoti iš kito CSV failo.

---

### Testavimas

Programa padengta unit testais naudojant `unittest` framework'ą. Iš viso – 22 testai apimantys `Person`, `User`, `Birthday` ir `BirthdayManager` klases.

```python
def test_no_duplicates(self):
    self.manager.add_birthday(self.birthday)
    self.manager.add_birthday(self.birthday)
    self.assertEqual(len(self.manager.get_all()), 1)

def test_singleton(self):
    manager2 = BirthdayManager()
    self.assertIs(self.manager, manager2)
```

Testai tikrina pagrindinį funkcionalumą: pridėjimą, ištrynimą, paiešką, Singleton veikimą, duplikatų blokavimą, amžiaus ir likusių dienų skaičiavimą.

---

## 3. Rezultatai ir išvados

### Rezultatai
- Sėkmingai sukurta gimtadienių priminimo programa su grafine vartotojo sąsaja (tkinter)
- Programa įgyvendina visus 4 OOP pilierius: inkapsuliacją, paveldimumą, polimorfizmą ir abstrakciją
- Naudojamas Singleton design pattern `BirthdayManager` klasėje užtikrinant vieną duomenų valdymo tašką
- Duomenys išsaugomi CSV faile ir išlieka tarp programos paleidimų, galimas eksportas ir importas
- 22 unit testai padengia pagrindinį programos funkcionalumą

### Išvados
Šio kursinio darbo metu sukurta funkcionali gimtadienių priminimo programa pritaikant OOP principus praktikoje. Programos architektūra yra aiški ir išplečiama – kiekviena klasė turi vieną konkrečią atsakomybę. Singleton pattern užtikrina duomenų vientisumą, agregacija ir kompozicija parodo skirtingus objektų ryšių tipus, o grafinis interfeisas su kalendoriumi, paieška ir spalviniu žymėjimu daro programą patogią naudoti.

### Programos plėtimo galimybės
- El. pašto pranešimų siuntimas automatiškai gimtadienio dieną
- Kelių vartotojų palaikymas su atskirais gimtadienių sąrašais
- Duomenų bazės (SQLite) naudojimas vietoj CSV
- Mobiliosios programėlės versija

---

## 4. Šaltiniai
- [Python dokumentacija](https://docs.python.org/3/)
- [tkinter dokumentacija](https://docs.python.org/3/library/tkinter.html)
- [tkcalendar dokumentacija](https://tkcalendar.readthedocs.io/)
- [unittest dokumentacija](https://docs.python.org/3/library/unittest.html)
- [PEP8 stilius](https://pep8.org/)
- [Design Patterns](https://refactoring.guru/design-patterns)