from collections import UserDict
import re
from datetime import datetime, timedelta

def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError:
            return "Invalid input. Please check your data."
        except IndexError:
            return "Missing arguments."
    return inner

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    pass

class Phone(Field):
    def __init__(self, value):
        if not re.fullmatch(r"\d{10}", value):
            raise ValueError("Phone number must contain exactly 10 digits.")
        super().__init__(value)

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return self.value.strftime("%d.%m.%Y")

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
        except ValueError as e:
            print(f"Error adding phone: {e}")

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, old_phone, new_phone):
        for p in self.phones:
            if p.value == old_phone:
                try:
                    p.value = Phone(new_phone).value
                    return
                except ValueError as e:
                    print(f"Error editing phone: {e}")
                    return
        print("Phone number not found.")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p
        return None

    def add_birthday(self, birthday):
        try:
            self.birthday = Birthday(birthday)
        except ValueError as e:
            print(f"Error adding birthday: {e}")

    def __str__(self):
        phones = "; ".join(p.value for p in self.phones)
        birthday = f", birthday: {self.birthday}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {phones}{birthday}"

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today()
        upcoming = []
        for record in self.data.values():
            if record.birthday:
                bday_this_year = record.birthday.value.replace(year=today.year)
                if bday_this_year < today:
                    bday_this_year = bday_this_year.replace(year=today.year + 1)
                delta_days = (bday_this_year - today).days
                if 0 <= delta_days < 7:
                    upcoming.append(f"{record.name.value}: {record.birthday}")
        return "\n".join(upcoming) if upcoming else "No upcoming birthdays."


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        command = input("Enter a command: ").strip().lower()

        if command in ["exit", "close"]:
            print("Goodbye!")
            break
        elif command == "hello":
            print("How can I help you?")
        elif command.startswith("add-birthday"):
            args = input("Enter name and birthday (DD.MM.YYYY): ").split()
            if len(args) < 2:
                print("Invalid input.")
                continue
            name, birthday = args
            record = book.find(name)
            if record:
                record.add_birthday(birthday)
                print("Birthday added.")
            else:
                print("Contact not found.")
        elif command.startswith("add"):
            args = input("Enter name and phone: ").split()
            if len(args) < 2:
                print("Invalid input.")
                continue
            name, phone = args[0], args[1]
            record = book.find(name) or Record(name)
            record.add_phone(phone)
            book.add_record(record)
            print("Contact saved.")
        elif command.startswith("change"):
            args = input("Enter name, old phone, new phone: ").split()
            if len(args) < 3:
                print("Invalid input.")
                continue
            name, old_phone, new_phone = args
            record = book.find(name)
            if record:
                record.edit_phone(old_phone, new_phone)
                print("Phone updated.")
            else:
                print("Contact not found.")
        elif command.startswith("phone"):
            args = input("Enter name: ").split()
            name = args[0] if args else ""
            record = book.find(name)
            print(record if record else "Contact not found.")
        elif command == "all":
            print("\n".join(str(r) for r in book.data.values()) or "No contacts found.")
        elif command.startswith("show-birthday"):
            args = input("Enter name: ").split()
            name = args[0] if args else ""
            record = book.find(name)
            print(record.birthday if record and record.birthday else "No birthday found.")
        elif command == "birthdays":
            print(book.get_upcoming_birthdays())
        else:
            print("Unknown command.")

if __name__ == "__main__":
    main()
