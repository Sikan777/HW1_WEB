from collections import UserDict
from datetime import datetime, timedelta
import pickle
import re

# Базовий клас Field для представлення поля зі значенням.
class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


# Клас Name успадкований від Field і представляє ім'я.
class Name(Field):
    def __init__(self, value):
        if not value:
            raise ValueError("Name cannot be empty")
        super().__init__(value)


# Клас Phone успадкований від Field і представляє номер телефону.
class Phone(Field):
    def __init__(self, value):
        self.value = value

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if (value.startswith('+') and len(value[1:]) == 12 and value[1:].isdigit()) or (
                value[1:].isdigit() and len(value) in (10, 12)):
            self._value = value
        else:
            raise ValueError('Invalid phone format')


# Клас Email успадкований від Field і представляє електронну адресу, з перевіркою валідності
class Email(Field):
    def __init__(self, value):
        self._value = value
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        if re.match(r"[A-Za-z][\w.]*@\w+\.\w{2,}", value):
            self._value = value
        else:
            raise ValueError('Invalid email format')

#клас Birthday для дня народження контакта (з перевіркою валідності)
class Birthday(Field):
    def __init__(self, value):
        self._value = value
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        try:
            self._value = datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Invalid date format for Birthday")

#клас Address для адреси контакта (з перевіркою валідності)
class Address(Field):
    def __init__(self, value):
        self._value = value
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):
        words = value.split()
        if len(words) >= 2 and all(len(word) > 3 for word in words):
            self._value = value
        else:
            raise ValueError('Invalid data format for Address')

# Клас Record для представлення контакту в адресній книзі.
class Record:
    def __init__(self, name, phone, email=None, address=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone)]
        self.emails = [Email(email)] if email else None
        self.address = Address(address) if address else None
        self.birthday = Birthday(birthday) if birthday else None

    # Додавання адреса до запису, якщо у записа вже є адрес - викликається помилка
    def add_address(self, address):
        if self.address is None:
            self.address = Address(address)
        else:
            raise ValueError("У цього записа вже існує адреса!")

    # Видалення адреса ( повернення до початкового стану як і був, тобто None )
    def remove_address(self):
        self.address = None

    # Редагування адреса, якщо такого не існує - викликається помилка
    def edit_address(self, old_address, new_address):
        if self.address.value == old_address:
            self.address.value = new_address
            return
        else:
            raise ValueError(f"Address '{old_address}' not found")

    # Додавання ел.пошти до списку ел.пошт записа
    def add_email(self, email):
        if self.emails is None:
            self.emails = []
        self.emails.append(Email(email))

    # Видалення ел.пошти із списка ел.пошт записа, якщо її не знайдено - викликається помилка
    def remove_email(self, email):
        for email in self.emails: #ітеруюся по списку імейлів
            if email.value == email: #перевірка, чи є даний імейл тому, який ми шукали
                self.emails.remove(email)
                return
        raise ValueError(f"Email '{email}' not found")

    # Редагування ел.пошти, якщо в списку такої немає - викликається помилка
    def edit_email(self, old_email, new_email):
        for email in self.emails: #ітеруюся по списку імейлів
            if email.value == old_email: #перевірка, чи є даний імейл тому, який ми шукали
                email.value = new_email
                return
        raise ValueError(f"Email '{old_email}' not found")

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    # Видалення тел. номера із списка номерів записа, якщо його не знайдено - викликається помилка
    def remove_phone(self, user_phone):
        for phone in self.phones: #ітеруюся по списку телефонів
            if phone.value == user_phone: #перевірка, чи є даний телефон тому, який ми шукали
                self.phones.remove(phone)
                return
        raise ValueError(f"Phone number '{user_phone}' not found")

    # Редагування тел. номера, якщо його не знайдено - викликається помилка
    def edit_phone(self, old_phone, new_phone):
        for phone in self.phones: #ітеруюся по списку телефонів
            if phone.value == old_phone:  #перевірка, чи є даний телефон тому, який ми шукали
                phone.value = new_phone
                return
        raise ValueError(f"Phone number '{old_phone}' not found")

    def find_phone(self, user_phone):
        # Пошук і повернення телефону за його номером.
        phones_found = [phone for phone in self.phones if phone.value == user_phone]
        return phones_found[0] if phones_found else None

    # Виводить всю інформацію про запис
    def __str__(self):
        attributes = [f"Contact name: {self.name.value}"]
        phones_str = '; '.join(str(phone) for phone in self.phones)
        attributes.append(f"Phones: {phones_str}")
        if self.emails:
            emails_str = '; '.join(str(email) for email in self.emails)
            attributes.append(f"Emails: {emails_str}")
        if self.address:
            attributes.append(f'Address: "{self.address.value}"')
        if self.birthday:
            attributes.append(f"Birthday: {self.birthday.value.date()}")
        return ', '.join(attributes)


# Клас AddressBook успадкований від UserDict і представляє адресну книгу.
class AddressBook(UserDict):
    def add_record(self, record):
        # Додає контакт до адресної книги, використовуючи ім'я контакту як ключ.
        self.data[record.name.value] = record

    def find(self, name):
        # Пошук і повернення контакту за ім'ям.
        if name in self.data:
            return self.data[name]

    def delete(self, name):
        # Видалення контакту з адресної книги за ім'ям.
        if name in self.data:
            del self.data[name]
            return f'{name}'

    def find_contact_with_phone(self, phone):
        for contact in self.data.values():
            if contact.find_phone(phone):
                return contact
        return None

    def __iter__(self):
        self.current_record = 0
        self.records = list(self.data.values())
        return self

    def __next__(self):
        if self.current_record < len(self.records):
            record = self.records[self.current_record]
            self.current_record += 1
            return record
        else:
            raise StopIteration

    def search(self, query):
        matches_found = []
        for record in self.data.values():
            if (
                    query.lower() in record.name.value.lower() or
                    any(query.lower() in phone.value for phone in record.phones)
            ):
                matches_found.append(record)
        return matches_found

    def save_to_file(self, filename):
        with open(filename, 'wb') as file:
            pickle.dump(self.data, file)

    def load_from_file(self, filename):
        try:
            with open(filename, 'rb') as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            self.data = {}

    # Метод days_to_birthday який виводить список контактів, у яких день народження через задану кількість днів
    # від поточної дати
    def days_to_birthday(self, days_to_filter):
        today = datetime.now().date()
        future_date = today + timedelta(days=days_to_filter)
        upcoming_birthdays = []
        for record in self.data.values():
            if record.birthday:
                next_birthday = datetime.strptime(record.birthday.value, "%Y-%m-%d").date().replace(year=today.year)
                if today > next_birthday:
                    next_birthday = next_birthday.replace(year=today.year + 1)
                if today <= next_birthday <= future_date:
                    upcoming_birthdays.append(str(record))
        if upcoming_birthdays:
            print(f'Співпадіння знайдені з такими контактами: {upcoming_birthdays}')
        else:
            print("Немає збігів.")
        return upcoming_birthdays


if __name__ == "__main__":
    # Створення адресної книги під час запуску скрипта.
    address_book = AddressBook()
    john_record = Record("John", '+380676753412', email='sdf@mail.ua',
                         birthday='2024-02-29')
    john_record.add_phone('+380676753411')
