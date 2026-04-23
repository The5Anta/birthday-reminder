import tkinter as tk
from tkinter import messagebox
from datetime import date
from models.person import Person
from models.birthday import Birthday
from manager.birthday_manager import BirthdayManager
from utils.file_handler import FileHandler
from utils.notification import NotificationChecker

FILE_PATH = "data/birthdays.csv"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Birthday Reminder")
        self.root.geometry("600x550")

        self.manager = BirthdayManager()
        self.file_handler = FileHandler(FILE_PATH)
        self.notifier = NotificationChecker()
        self._editing_index = None

        for b in self.file_handler.load():
            self.manager.add_birthday(b)

        self._build_ui()
        self._check_todays()

    def _build_ui(self):
        # Forma
        form = tk.LabelFrame(self.root, text="Gimtadienis", padx=10, pady=10)
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="Vardas:").grid(row=0, column=0, sticky="w")
        self.name_var = tk.StringVar()
        tk.Entry(form, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5)

        tk.Label(form, text="El. paštas:").grid(row=1, column=0, sticky="w")
        self.email_var = tk.StringVar()
        tk.Entry(form, textvariable=self.email_var, width=30).grid(row=1, column=1, padx=5)

        tk.Label(form, text="Data (YYYY-MM-DD):").grid(row=2, column=0, sticky="w")
        self.date_var = tk.StringVar()
        tk.Entry(form, textvariable=self.date_var, width=30).grid(row=2, column=1, padx=5)

        tk.Label(form, text="Pastaba:").grid(row=3, column=0, sticky="w")
        self.note_var = tk.StringVar()
        tk.Entry(form, textvariable=self.note_var, width=30).grid(row=3, column=1, padx=5)

        btn_frame = tk.Frame(form)
        btn_frame.grid(row=4, column=1, pady=5, sticky="e")

        self.save_btn = tk.Button(btn_frame, text="Išsaugoti", command=self._save)
        self.save_btn.pack(side="left", padx=3)

        self.cancel_btn = tk.Button(btn_frame, text="Atšaukti", command=self._cancel, state="disabled")
        self.cancel_btn.pack(side="left", padx=3)

        # Sąrašas
        list_frame = tk.LabelFrame(self.root, text="Gimtadieniai", padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.listbox = tk.Listbox(list_frame, height=10)
        self.listbox.pack(fill="both", expand=True)

        btn_frame2 = tk.Frame(list_frame)
        btn_frame2.pack(pady=5)

        tk.Button(btn_frame2, text="Redaguoti", command=self._edit).pack(side="left", padx=5)
        tk.Button(btn_frame2, text="Ištrinti", command=self._delete).pack(side="left", padx=5)

        self._refresh_list()

    def _save(self):
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        date_str = self.date_var.get().strip()
        note = self.note_var.get().strip()

        if not name or not email or not date_str:
            messagebox.showwarning("Klaida", "Užpildyk visus privalomus laukus.")
            return

        try:
            birth_date = date.fromisoformat(date_str)
        except ValueError:
            messagebox.showerror("Klaida", "Data turi būti YYYY-MM-DD formatu.")
            return

        person = Person(name, email)
        birthday = Birthday(person, birth_date, note)

        if self._editing_index is not None:
            birthdays = self.manager.get_all()
            old_name = birthdays[self._editing_index].person.name
            self.manager.remove_birthday(old_name)
            self.manager.get_all().insert(self._editing_index, birthday)
            self._editing_index = None
            self.cancel_btn.config(state="disabled")
            self.save_btn.config(text="Išsaugoti")
        else:
            self.manager.add_birthday(birthday)

        self.file_handler.save(self.manager.get_all())
        self._clear_form()
        self._refresh_list()

    def _edit(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Klaida", "Pasirink gimtadienį iš sąrašo.")
            return

        index = selected[0]
        self._editing_index = index
        b = self.manager.get_all()[index]

        self.name_var.set(b.person.name)
        self.email_var.set(b.person.email)
        self.date_var.set(b.birth_date.isoformat())
        self.note_var.set(b.note)

        self.save_btn.config(text="Atnaujinti")
        self.cancel_btn.config(state="normal")

    def _delete(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Klaida", "Pasirink gimtadienį iš sąrašo.")
            return
        index = selected[0]
        birthday = self.manager.get_all()[index]
        self.manager.remove_birthday(birthday.person.name)
        self.file_handler.save(self.manager.get_all())
        self._editing_index = None
        self._clear_form()
        self._refresh_list()

    def _cancel(self):
        self._editing_index = None
        self._clear_form()
        self.save_btn.config(text="Išsaugoti")
        self.cancel_btn.config(state="disabled")

    def _clear_form(self):
        self.name_var.set("")
        self.email_var.set("")
        self.date_var.set("")
        self.note_var.set("")

    def _refresh_list(self):
        self.listbox.delete(0, tk.END)
        for b in self.manager.get_all():
            self.listbox.insert(tk.END, str(b))

    def _check_todays(self):
        todays = self.notifier.check(self.manager.get_all())
        if todays:
            names = ", ".join(b.person.name for b in todays)
            messagebox.showinfo("🎂 Gimtadienis!", f"Šiandien gimtadienis: {names}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()