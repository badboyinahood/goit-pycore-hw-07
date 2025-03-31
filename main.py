from collections import UserDict
import re
from datetime import datetime, timedelta


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
        birthday_str = f", birthday: {self.birthday.value.strftime('%d.%m.%Y')}" if self.birthday else ""
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}{birthday_str}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def get_upcoming_birthdays(self):
        today = datetime.today().date()
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                bday = record.birthday.value.date().replace(year=today.year)
                if bday < today:
                    bday = bday.replace(year=today.year + 1)
                delta_days = (bday - today).days
                if delta_days < 7:
                    upcoming_birthdays.append((record.name.value, bday.strftime("%d.%m.%Y")))
        return upcoming_birthdays


# Приклад використання
if __name__ == "__main__":
    book = AddressBook()

    try:
        # Створення запису для John
        john_record = Record("John")
        john_record.add_phone("1234567890")
        john_record.add_phone("5555555555")
        john_record.add_birthday("15.04.1990")
        book.add_record(john_record)

        # Створення запису для Jane
        jane_record = Record("Jane")
        jane_record.add_phone("9876543210")
        jane_record.add_birthday("20.04.1992")
        book.add_record(jane_record)

        # Виведення всіх записів
        for name, record in book.data.items():
            print(record)

        # Редагування телефону John
        john = book.find("John")
        if john:
            john.edit_phone("1234567890", "1112223333")
            print(john)

        # Пошук телефону у записі John
        if john:
            found_phone = john.find_phone("5555555555")
            print(f"{john.name}: {found_phone}")

        # Видалення запису Jane
        book.delete("Jane")

        # Показ днів народження на наступному тижні
        upcoming = book.get_upcoming_birthdays()
        print("Upcoming birthdays:")
        for name, bday in upcoming:
            print(f"{name}: {bday}")

    except Exception as e:
        print(f"Unexpected error: {e}")
