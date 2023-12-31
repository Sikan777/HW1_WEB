from SotedFileLogick import select_and_sort_folder
from tkinter import simpledialog

# from tkinter import messagebox
import tkinter as tk
from AdressBookLogick import AddressBook, Record, Phone, Email
import NotesLogick as nl  # импорт всего модуля, ибо основные функции там не в классе
from abc import abstractmethod, ABC

def get_contact_info(info_type):
    contact_info = simpledialog.askstring(
        "Добавление контакта", f"Введите {info_type} (если нет - закрой окно):"
    )
    return contact_info if contact_info else None


def contact_name_request(name):
    contact = simpledialog.askstring("Введи имя контакта:", f"Введите {name}")
    return contact if contact else None

class Processor(ABC):
    @abstractmethod
    def process_command(self, command):
        pass

    @abstractmethod
    def execute_command(self):
        pass

    @abstractmethod
    def on_closing(self):
        pass

class CommandProcessorApp(Processor):
    def __init__(
            self, app, address_book, notes_book
    ):  # Добавила список заметок как аргумент в класс
        self.app = app
        self.address_book = address_book
        self.notes_book = notes_book
        self.app.geometry("500x500")
        self.app.configure(bg="#F5F5DC")
        self.app.title("Твой помошник 😊")

        # Создание метки для инструкций пользователя
        commands = [
            "add",
            "find contact",
            "check birthday",
            "search",
            "delete",
            "add phone",
            "add address",
            "remove address",
            "edit address",
            "remove phone",
            "edit phone",
            "find phone",
            "add email",
            "edit email",
            "remove email",
            "note",
            "search note",
            "edit note",
            "update note",
            "add tag",
            "with tag",
            "sort note",
            "remove note",
            "show note",
        ]

        descriptions = [
            "Добавить контакт",
            "Найти контакт по имени",
            "Проверить день рождения",
            "Поиск",
            "Удалить контакт",
            "Добавить телефон",
            "Добавить адрес",
            "Удалить адрес",
            "Редактировать адрес",
            "Удалить телефон",
            "Редактировать телефон",
            "Найти телефон",
            "Добавить почту",
            "Редактировать почту",
            "Удалить почту",
            "Добавить заметку",
            "Поиск заметки",
            "Редактировать заметку",
            "Обновить заметку",
            "Добавить тег к заметке",
            "Отобразить заметки с тегом",
            "Сортировать заметки",
            "Удалить заметку",
            "Показать заметку",
        ]

        # Создаем метку для перечня команд
        commands_label = tk.Label(
            app,
            text="Список команд:",
            background="#F5F5DC",
            justify="left"
        )
        commands_label.pack()

        # Создаем текстовое поле для перечня команд и описаний
        commands_text = tk.Text(
            app,
            wrap="word",
            height=10,
            width=40,
            background="#F5F5DC"
        )
        commands_text.pack()

        # Вставляем команды и описания в текстовое поле
        for command, description in zip(commands, descriptions):
            commands_text.insert(tk.END, f"{command} - {description}\n")

        # Создаем метку для ввода команды
        self.input_label = tk.Label(
            app,
            text="Введите команду:",
            background="#F5F5DC"
        )
        self.input_label.pack()

        # Создаем виджет ввода для пользователя
        self.input_entry = tk.Entry(app)
        self.input_entry.pack()

        # Создаем кнопку "Выполнить" и привязываем ее к функции execute_command
        self.submit_button = tk.Button(
            app,
            text="Выполнить",
            command=self.execute_command
        )
        self.submit_button.pack()

        # Создаем метку для вывода результата
        self.result_label = tk.Label(app, text="")
        self.result_label.pack()

        self.app.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.error_label = tk.Label(
            self.app,
            text="",
            foreground="red",
            background="#F5F5DC"
        )
        self.error_label.pack()

    def process_command(self, command):
        # Функция обработки команды
        if command == "sorted path":
            return select_and_sort_folder()
        elif command == "add":
            return self.add_contact()
        elif command == "find contact":
            return self.find_contact()
        elif command == "check birthday":
            return self.birthday()
        elif command == "search":
            return self.search_contact()
        elif command == "delete":
            return self.delete_contact()
        elif command == "add phone":
            return self.add_phone_to_contact()
        elif command == "add address":
            return self.add_address()
        elif command == "remove address":
            return self.remove_address_from_contact()
        elif command == "edit address":
            return self.edit_address()
        elif command == "remove phone":
            return self.remove_phone_in_contact()
        elif command == "edit phone":
            return self.edit_phone_contact()
        elif command == "find phone":
            return self.find_phone_contact()
        elif command == "add email":
            return self.add_email()
        elif command == "edit email":
            return self.edit_email()
        elif command == "remove email":
            return self.remove_email_in_contact()
        # Здесь добавила команды для заметок
        elif command == "note":
            return self.add_note()
        elif command == "search note":
            return self.search_note()
        elif command == "edit note":
            return self.edit_note()
        elif command == "update note":
            return self.update_note()
        elif command == "add tag":
            return self.add_tag()
        elif command == "with tag":
            return self.with_tag()
        elif command == "sort note":
            return self.sort_note()
        elif command == "remove note":
            return self.remove_note()
        elif command == "show note":
            return self.show_note()

    def show_note(self):  # показывает все заметки
        return nl.show_all_notes(notes_book)

    def add_note(self):  # добавляет заметку
        title = simpledialog.askstring("Добавление заметки", "Введите заголовок:")
        content = simpledialog.askstring("Добавление заметки", "Введите заметку:")
        return nl.add_note(notes_book, content, title)

    def search_note(self):  # ищет заметку рандомному слову
        word = simpledialog.askstring("Поиск заметки", "Введите поисковое слово:")
        return nl.search_notes(notes_book, word)

    def edit_note(self):  # полностью переписывает заметку, находя ее по заголовку
        title = simpledialog.askstring("Изменение заметки", "Введите заголовок:")
        content = simpledialog.askstring("Изменение заметки", "Введите новую заметку:")
        return nl.edit_note(notes_book, title, content)

    def update_note(self):  # дописывает текст в существующую заметку
        title = simpledialog.askstring("Дозапись заметки", "Введите заголовок:")
        content = simpledialog.askstring("Дозапись заметки", "Введите текст:")
        return nl.add_existing_note(notes_book, title, content)

    def add_tag(self):  # добавляет тэги в существующую заметку
        title = simpledialog.askstring("Добавление тэга заметки", "Введите заголовок:")
        tag = simpledialog.askstring("Добавление тэга заметки", "Введите тэг:")
        return nl.add_tag(notes_book, title, tag)

    def with_tag(self):  # находит заметку по тэгу, пока что не работает, исправим позже
        tag = simpledialog.askstring("Поиск заметок по тэгу", "Введите тэг:")
        return nl.search_by_tag(notes_book, tag)

    def sort_note(self):  # сортирует заметки по дате добавления
        return nl.sort_notes(notes_book)

    def remove_note(self):  # удаляет заметку по ее заголовку
        title = simpledialog.askstring("Удаление заметки", "Введите заголовок:")
        return nl.remove_note(notes_book, title)

    def find_contact(self):  # Поиск контакта
        contact_name = contact_name_request("Имя")
        try:
            contact = address_book.find(contact_name)
            if contact:
                self.error_label.config(text="")
                return f"Контакт, который вы искали: {contact}"
            else:
                self.error_label.config(
                    text=f"Контакт с именем {contact_name} не найден"
                )
        except ValueError as e:
            self.error_label.config(text=str(e))

    def add_email(self):
        contact_name = simpledialog.askstring(
            "Добавление почтового ящика", "Введите имя контакта:"
        )
        if contact_name:
            contact = self.address_book.find(contact_name)
            if contact:
                new_email = simpledialog.askstring(
                    "Добавление почтового ящика", "Введите новый почтовый адрес:"
                )
                if new_email:
                    try:
                        contact.add_email(
                            new_email
                        )  # Создаем экземпляр Email и добавляем его к контакту
                        return f"Вы добавили почтовый адрес {new_email} для {contact}."
                    except ValueError as e:
                        self.error_label.config(text=str(e))
                else:
                    self.error_label.config(text="Вы не ввели новый почтовый адрес.")
            else:
                self.error_label.config(
                    text=f"Контакт с именем {contact_name} не найден."
                )
        else:
            self.error_label.config(text="Вы не ввели имя контакта.")

    def edit_email(self):
        user_input = simpledialog.askstring("Ввод данных", "Введите имя контакта")
        if user_input:
            contact = self.address_book.find(user_input)
            if contact:
                if contact.emails:
                    old_email = simpledialog.askstring(
                        "Ввод данных", "Введите старую почту"
                    )
                    if old_email:
                        new_email = simpledialog.askstring(
                            "Ввод данных", "Введите новую почту"
                        )
                        if new_email:
                            try:
                                Email(new_email)
                                contact.edit_email(old_email, new_email)
                                return f"Вы изменили номер телефона у контакта {contact.name}: {old_email} -> {new_email}"
                            except ValueError as e:
                                self.error_label.config(text=str(e))
                        else:
                            self.error_label.config(
                                text="Введите новый почтовый адрес."
                            )
                    else:
                        self.error_label.config(text="Введите старый почтовый адрес.")
                else:
                    self.error_label.config(text=f"{contact} не имеет почтового адреса")
            else:
                self.error_label.config(text=f"Контакт {contact} не найден")
        else:
            self.error_label.config(text="Вы не ввели имя контакта.")

    def remove_email_in_contact(self):
        contact_name = simpledialog.askstring("Удаление почты", "Введите имя контакта:")
        if contact_name:
            contact = self.address_book.find(contact_name)
            if contact:
                removed_email = simpledialog.askstring(
                    "Удаление почты", f"Введите почту для контакта {contact_name}:"
                )
                try:
                    contact.remove_email(removed_email)
                    return f'Вы удалили почту "{removed_email}" для контакта "{contact_name}".'
                except ValueError as e:
                    self.error_label.config(text=str(e))
            else:
                self.error_label.config(
                    text=f"Контакт с именем {contact_name} не найден."
                )
        else:
            self.error_label.config(text="Введите имя контакта.")

    def add_contact(self):
        contact_name = simpledialog.askstring("Добавление контакта", "Введите имя контакта:")
        contact_phone = simpledialog.askstring("Добавление контакта", "Введите номер контакта:")

        # Проверка формата номера телефона
        try:
            Phone(contact_phone)  # Если прошло проверку формата, ничего не произойдет
        except ValueError as e:
            self.error_label.config(text=str(e))
            return

        contact_mail = get_contact_info("почту контакта")

        # Проверка формата email
        if contact_mail is not None:  # Пользователь ввел email или нажал Отмена
            try:
                Email(contact_mail)  # Если прошло проверку формата, ничего не произойдет
            except ValueError as e:
                self.error_label.config(text=str(e))
                return
        else:
            contact_mail = None

        contact_address = get_contact_info("адрес контакта")
        contact_birthday = get_contact_info("день рождения контакта")

        contact = Record(contact_name, contact_phone, email=contact_mail, address=contact_address,
                         birthday=contact_birthday)

        self.address_book.add_record(contact)

        return f'Вы добавили новый контакт: {contact_name} - {contact_phone}'

        # if contact_name and contact_phone: contact = Record(contact_name, contact_phone, email=contact_mail,
        # address=contact_address, birthday=contact_birthday) self.address_book.add_record(contact) return f'Вы
        # добавили новый контакт: {contact_name} - {contact_phone}'

    def add_phone_to_contact(self):
        contact_name = simpledialog.askstring(
            "Добавление номера телефона", "Введите имя контакта:"
        )
        if contact_name:
            contact = self.address_book.find(contact_name)
            if contact:
                phone_number = simpledialog.askstring(
                    "Добавление номера телефона", "Введите номер телефона:"
                )
                try:
                    Phone(phone_number)
                    contact.add_phone(phone_number)
                    # self.error_label.config(text=f'Вы добавили номер телефона для {contact_name}.')
                    return (
                        f"Вы добавили номер телефона {phone_number} для {contact_name}."
                    )
                except ValueError as e:
                    self.error_label.config(text=str(e))
            else:
                self.error_label.config(
                    text=f"Контакт с именем {contact_name} не найден."
                )
        else:
            self.error_label.config(text="Введите имя контакта.")

    def edit_phone_contact(self):
        user_input = simpledialog.askstring("Выбор контакта", "Введите имя контакта:")
        if user_input:
            contact = self.address_book.find(user_input)
            if contact:
                if contact.phones:
                    old_phone = simpledialog.askstring(
                        "Редактирование телефона", "Введите старый номер телефона:"
                    )
                    if old_phone:
                        new_phone = simpledialog.askstring(
                            "Редактирование телефона", "Введите новый номер телефона:"
                        )
                        if new_phone:
                            try:
                                # Проверка формата нового номера (вызывает исключение, если формат неверен)
                                Phone(new_phone)
                                # Обновление номера у объекта contact
                                contact.phone.value = new_phone
                                return f"Вы изменили номер телефона у контакта {contact.name}: {old_phone} -> {new_phone}"
                            except ValueError as e:
                                self.error_label.config(text=str(e))
                        else:
                            self.error_label.config(
                                text="Введите новый номер телефона."
                            )
                    else:
                        self.error_label.config(text="Введите старый номер телефона.")
                else:
                    self.error_label.config(text=f"{contact} не имеет телефона")
            else:
                self.error_label.config(text=f"Контакт {user_input} не найден")
        else:
            self.error_label.config(text="Вы не ввели имя контакта.")

    def remove_phone_in_contact(self):
        contact_name = simpledialog.askstring(
            "Удаление телефона", "Введите имя контакта:"
        )
        if contact_name:
            contact = self.address_book.find(contact_name)
            if contact:
                removed_phone = simpledialog.askstring(
                    "Удаление телефона",
                    f"Введите номер телефона для контакта {contact_name}:",
                )
                try:
                    contact.remove_phone(removed_phone)
                    return f'Вы удалили телефон "{removed_phone}" для контакта "{contact_name}".'
                except ValueError as e:
                    self.error_label.config(text=str(e))
            else:
                self.error_label.config(
                    text=f"Контакт с именем {contact_name} не найден."
                )
        else:
            self.error_label.config(text="Введите имя контакта.")

    def find_phone_contact(self):
        user_input = simpledialog.askstring(
            "Поиск номера телефона", "Введите номер телефона:"
        )
        if user_input:
            contact = self.address_book.find_contact_with_phone(user_input)
            if contact:
                return f"Найден контакт с номером телефона {user_input}: {contact.name}"
            else:
                return f"Контакт с номером телефона {user_input} не найден."
        else:
            self.error_label.config(text="Введите номер телефона.")

    def add_address(self):
        contact_name = simpledialog.askstring(
            "Добалвение адреса", "Введите имя контакта:"
        )
        if contact_name:
            contact = self.address_book.find(contact_name)
            if contact:
                contact_address = simpledialog.askstring(
                    "Добалвение адреса", "Введите адрес:"
                )
                try:
                    contact.add_address(contact_address)
                    return f"Вы добавили адрес {contact_address} для {contact_name}."
                except ValueError as e:
                    self.error_label.config(text=str(e))
            else:
                self.error_label.config(
                    text=f"Контакт с именем {contact_name} не найден."
                )
        else:
            self.error_label.config(text="Введите имя контакта.")

    def remove_address_from_contact(self):
        contact_name = simpledialog.askstring(
            "Удаление адреса", "Введите имя контакта:"
        )
        if contact_name:
            contact = self.address_book.find(contact_name)
            if contact:
                if contact.address is not None:
                    removed_address = contact.address.value
                    contact.remove_address()
                    return f'Вы удалили адрес "{removed_address}" для контакта "{contact_name}".'
                else:
                    self.error_label.config(text=f"{contact_name} не имеет адреса.")
            else:
                self.error_label.config(
                    text=f"Контакт с именем {contact_name} не найден."
                )
        else:
            self.error_label.config(text="Введите имя контакта.")

    def edit_address(self):
        user_input = simpledialog.askstring("Выбор каогтакта", "Введите имя контакте:")
        if user_input:
            contact = self.address_book.find(user_input)
            if contact:
                if contact.address:
                    old_address = simpledialog.askstring(
                        "Редактирование адреса", "Введите старый адрес:"
                    )
                    new_address = simpledialog.askstring(
                        "Редактирование адреса", "Введите новый адрес:"
                    )
                    if old_address and new_address:
                        try:
                            contact.edit_address(old_address, new_address)
                            return f"Вы изменили адрес у контакта {contact.name}: {old_address} -> {new_address}"
                        except ValueError as e:
                            self.error_label.config(text=str(e))
                    else:
                        self.error_label.config(
                            text=f"Пожалуйста, введите и старый адрес, и новый адрес."
                        )
                else:
                    self.error_label.config(text=f"{contact} не имеет адреса")
            else:
                self.error_label.config(text=f"Контакт {contact} не найден")
        else:
            self.error_label.config(text="Вы не ввели контакт для адреса")

    def delete_contact(self):
        user_input = simpledialog.askstring(
            "Удаление контакта", "Введите имя контакта для удаления:"
        )
        if user_input:
            result = self.address_book.delete(user_input)
            if result:
                self.error_label.config(text=f"Вы удалили контакт: {result}")
            else:
                self.error_label.config(text="Контакт не найден")

    def search_contact(self):
        user_input = simpledialog.askstring("Окно ввода", "Введите данные для поиска:")
        if user_input:
            matches = self.address_book.search(user_input)
            if matches:
                result = "Найдены совпадения в таких контактах:\n"
                result += "\n".join(str(record) for record in matches)
                return result
            else:
                return "Совпадений не найдено."

    def birthday(self):
        try:
            days = int(
                simpledialog.askstring(
                    "Проверка дней рождения", "Введите количество дней:"
                )
            )
            if isinstance(days, int):
                upcoming_birthdays = self.address_book.days_to_birthday(days)
                if upcoming_birthdays:
                    return f"Співпадіння знайдені з такими контактами:\n" + "\n".join(
                        upcoming_birthdays
                    )
                else:
                    return "Немає збігів."
            else:
                return f"{days} - дорогой, нужно вводить количество дней в числовом формате."
        except ValueError:
            return (
                "Неправильный формат ввода. Введите количество дней в числовом формате."
            )

    def execute_command(self):
        # Функция, вызываемая при нажатии кнопки "Выполнить"
        user_input = self.input_entry.get()  # Получаем текст из виджета Entry
        result = self.process_command(user_input)  # Обрабатываем команду
        self.result_label.config(text=result)  # Обновляем виджет Label с результатом

    def on_closing(self):
        # Обработчик закрытия окна
        self.address_book.save_to_file("address-book")  # Сохраняем данные в файл
        nl.send_to_system(self.notes_book, "notes-book")  # Сохраняем данные в файл
        self.app.destroy()


if __name__ == "__main__":
    import os

    data_folder = "data"
    if not os.path.exists(data_folder):
        os.mkdir(data_folder)

    address_book = AddressBook()
    notes_book = nl.NotesBook()
    address_book_file = os.path.join(data_folder, "address-book")
    notes_book_file = os.path.join(data_folder, "notes-book")

    address_book.load_from_file(address_book_file)
    nl.get_from_system(notes_book, notes_book_file)

    app = tk.Tk()
    command_processor = CommandProcessorApp(
        app, address_book, notes_book
    )
    app.mainloop()

    # После завершения работы приложения, можно сохранить данные
    address_book.save_to_file(address_book_file)
    nl.save_to_system(notes_book, notes_book_file)
