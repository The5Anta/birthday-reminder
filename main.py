import tkinter as tk
from tkinter import messagebox, ttk
from tkcalendar import DateEntry, Calendar
from datetime import date
from models.person import Person
from models.birthday import Birthday
from manager.birthday_manager import BirthdayManager
from utils.file_handler import FileHandler
from utils.notification import NotificationChecker
from tkinter import filedialog

FILE_PATH = "data/birthdays.csv"


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Birthday Reminder")
        self.root.geometry("650x650")

        self.manager = BirthdayManager()
        self.file_handler = FileHandler(FILE_PATH)
        self.notifier = NotificationChecker()
        self._editing_index = None

        for b in self.file_handler.load():
            self.manager.add_birthday(b)

        self._build_ui()
        self._check_todays()

    def _build_ui(self):
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)

        self.main_frame = tk.Frame(notebook)
        self.cal_frame = tk.Frame(notebook)

        notebook.add(self.main_frame, text="🎂 Gimtadieniai")
        notebook.add(self.cal_frame, text="📅 Kalendorius")

        notebook.bind("<<NotebookTabChanged>>", lambda e: self._refresh_calendar())

        self._build_main_tab()
        self._build_calendar_tab()

    def _build_main_tab(self):
        # Forma
        form = tk.LabelFrame(self.main_frame, text="Gimtadienis", padx=10, pady=10)
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="Vardas:").grid(row=0, column=0, sticky="w")
        self.name_var = tk.StringVar()
        tk.Entry(form, textvariable=self.name_var, width=30).grid(row=0, column=1, padx=5)

        tk.Label(form, text="El. paštas:").grid(row=1, column=0, sticky="w")
        self.email_var = tk.StringVar()
        tk.Entry(form, textvariable=self.email_var, width=30).grid(row=1, column=1, padx=5)

        tk.Label(form, text="Gimimo data:").grid(row=2, column=0, sticky="w")
        self.date_entry = DateEntry(form, width=28, date_pattern="yyyy-mm-dd",
                                   maxdate=date.today())
        self.date_entry.grid(row=2, column=1, padx=5, pady=3)

        tk.Label(form, text="Pastaba:").grid(row=3, column=0, sticky="w")
        self.note_var = tk.StringVar()
        tk.Entry(form, textvariable=self.note_var, width=30).grid(row=3, column=1, padx=5)

        tk.Label(form, text="Priminti likus dienų:").grid(row=4, column=0, sticky="w")
        self.reminder_var = tk.StringVar(value="7")
        tk.Entry(form, textvariable=self.reminder_var, width=10).grid(row=4, column=1, padx=5, sticky="w")

        btn_frame = tk.Frame(form)
        btn_frame.grid(row=5, column=1, pady=5, sticky="e")

        self.save_btn = tk.Button(btn_frame, text="Išsaugoti", command=self._save)
        self.save_btn.pack(side="left", padx=3)

        self.cancel_btn = tk.Button(btn_frame, text="Atšaukti", command=self._cancel, state="disabled")
        self.cancel_btn.pack(side="left", padx=3)

        # Paieška
        search_frame = tk.Frame(self.main_frame)
        search_frame.pack(fill="x", padx=10)
        tk.Label(search_frame, text="🔍 Paieška:").pack(side="left")
        self.search_var = tk.StringVar()
        self.search_var.trace("w", lambda *args: self._refresh_list())
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side="left", padx=5)

        # Sąrašas
        list_frame = tk.LabelFrame(self.main_frame, text="Gimtadieniai", padx=10, pady=10)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)

        self.listbox = tk.Listbox(list_frame, height=10)
        self.listbox.pack(fill="both", expand=True)

        legend = tk.Frame(list_frame)
        legend.pack(anchor="w", pady=2)
        tk.Label(legend, text="■", fg="green").pack(side="left")
        tk.Label(legend, text="Šiandien  ").pack(side="left")
        tk.Label(legend, text="■", fg="orange").pack(side="left")
        tk.Label(legend, text="Per 7 dienas  ").pack(side="left")

        btn_frame2 = tk.Frame(list_frame)
        btn_frame2.pack(pady=5)
        tk.Button(btn_frame2, text="Redaguoti", command=self._edit).pack(side="left", padx=5)
        tk.Button(btn_frame2, text="Ištrinti", command=self._delete).pack(side="left", padx=5)
        btn_frame3 = tk.Frame(list_frame)
        btn_frame3.pack(pady=2)
        tk.Button(btn_frame3, text="📤 Eksportuoti CSV", command=self._export).pack(side="left", padx=5)
        tk.Button(btn_frame3, text="📥 Importuoti CSV", command=self._import).pack(side="left", padx=5)

        self._refresh_list()

    def _build_calendar_tab(self):
        self.calendar = Calendar(self.cal_frame, selectmode="day",
                                 date_pattern="yyyy-mm-dd",
                                 showweeknumbers=False)
        self.calendar.pack(fill="both", expand=True, padx=10, pady=10)

        self.cal_info = tk.Label(self.cal_frame, text="", font=("Arial", 11))
        self.cal_info.pack(pady=5)

        self.calendar.bind("<<CalendarSelected>>", self._on_date_selected)
        self._refresh_calendar()

    def _refresh_calendar(self):
        self.calendar.calevent_remove("all")

        today = date.today()
        for b in self.manager.get_all():
            for year in [today.year - 1, today.year, today.year + 1]:
                try:
                    birthday_date = b.birth_date.replace(year=year)
                    self.calendar.calevent_create(birthday_date, b.person.name, "birthday")
                except ValueError:
                    pass

        self.calendar.tag_config("birthday", background="#90e371", foreground="white")

    def _on_date_selected(self, event):
        selected_str = self.calendar.get_date()
        selected = date.fromisoformat(selected_str)
        matches = [b for b in self.manager.get_all()
                   if b.birth_date.month == selected.month and b.birth_date.day == selected.day]
        if matches:
            info = "\n".join(f"🎂 {b.person.name} – {b.age()} m." for b in matches)
            self.cal_info.config(text=info)
        else:
            self.cal_info.config(text="")

    def _get_sorted_filtered(self):
        query = self.search_var.get().strip().lower()
        birthdays = self.manager.get_all()
        if query:
            birthdays = [b for b in birthdays if query in b.person.name.lower()]
        return sorted(birthdays, key=lambda b: b.days_until())

    def _refresh_list(self):
        self.listbox.delete(0, tk.END)
        for b in self._get_sorted_filtered():
            days = b.days_until()
            age = b.age()
            label = f"{b.person.name} | {b.birth_date} | {age} m. | liko {days} d."
            if b.note:
                label += f" | {b.note}"
            self.listbox.insert(tk.END, label)
            if days == 0:
                self.listbox.itemconfig(tk.END, fg="green")
            elif days <= 7:
                self.listbox.itemconfig(tk.END, fg="orange")

    def _check_reminders(self):
        try:
            days_threshold = int(self.reminder_var.get())
        except ValueError:
            days_threshold = 7
        upcoming = [b for b in self.manager.get_all() if 0 < b.days_until() <= days_threshold]
        if upcoming:
            names = "\n".join(f"{b.person.name} – liko {b.days_until()} d." for b in upcoming)
            messagebox.showinfo("🔔 Artėjantys gimtadieniai", names)

    def _save(self):
        name = self.name_var.get().strip()
        email = self.email_var.get().strip()
        date_str = self.date_entry.get()
        note = self.note_var.get().strip()

        if not name or not email:
            messagebox.showwarning("Klaida", "Užpildyk visus privalomus laukus.")
            return

        if "@" not in email or "." not in email.split("@")[-1]:
            messagebox.showerror("Klaida", "Neteisingas el. pašto formatas.")
            return

        try:
            birth_date = date.fromisoformat(date_str)
        except ValueError:
            messagebox.showerror("Klaida", "Neteisingas datos formatas.")
            return
        if not all(c.isalpha() or c.isspace() for c in name):
            messagebox.showerror("Klaida", "Vardas gali turėti tik raides.")
            return

        person = Person(name, email)
        birthday = Birthday(person, birth_date, note)

        if self._editing_index is not None:
            sorted_b = self._get_sorted_filtered()
            old_name = sorted_b[self._editing_index].person.name
            self.manager.remove_birthday(old_name)
            self.manager.add_birthday(birthday)
            self._editing_index = None
            self.cancel_btn.config(state="disabled")
            self.save_btn.config(text="Išsaugoti")
        else:
            added = self.manager.add_birthday(birthday)
            if not added:
                messagebox.showwarning("Klaida", "Toks įrašas jau egzistuoja.")
                return
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
        b = self._get_sorted_filtered()[index]

        self.name_var.set(b.person.name)
        self.email_var.set(b.person.email)
        self.date_entry.set_date(b.birth_date)
        self.note_var.set(b.note)

        self.save_btn.config(text="Atnaujinti")
        self.cancel_btn.config(state="normal")

    def _delete(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Klaida", "Pasirink gimtadienį iš sąrašo.")
            return
        index = selected[0]
        b = self._get_sorted_filtered()[index]
        self.manager.remove_birthday(b.person.name)
        self.file_handler.save(self.manager.get_all())
        self._editing_index = None
        self._clear_form()
        self._refresh_list()

    def _cancel(self):
        self._editing_index = None
        self._clear_form()
        self.save_btn.config(text="Išsaugoti")
        self.cancel_btn.config(state="disabled")

    def _export(self):
        filepath = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV failai", "*.csv")],
            title="Eksportuoti gimtadienius"
        )
        if filepath:
            FileHandler(filepath).save(self.manager.get_all())
            messagebox.showinfo("Sėkmė", "Gimtadieniai eksportuoti!")

    def _import(self):
        filepath = filedialog.askopenfilename(
            filetypes=[("CSV failai", "*.csv")],
            title="Importuoti gimtadienius"
        )
        if filepath:
            birthdays = FileHandler(filepath).load()
            for b in birthdays:
                self.manager.add_birthday(b)
            self.file_handler.save(self.manager.get_all())
            self._refresh_list()
            self._refresh_calendar()
            messagebox.showinfo("Sėkmė", f"Importuota {len(birthdays)} įrašų!")
    def _clear_form(self):
        self.name_var.set("")
        self.email_var.set("")
        self.date_entry.set_date(date.today())
        self.note_var.set("")

    def _check_todays(self):
        todays = self.notifier.check(self.manager.get_all())
        if todays:
            names = ", ".join(b.person.name for b in todays)
            messagebox.showinfo("🎂 Gimtadienis!", f"Šiandien gimtadienis: {names}")


if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()