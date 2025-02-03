'''Консольний бот помічник, який використовує реалізовані класи для
управління адресною книгою.
'''

from contacts import AddressBook, Record, AddressBookValueError


def input_error(func):
    '''Декоратор обробки помилок'''
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except AddressBookValueError as err:
            return str(err)
        except ValueError:
            return "Give me name and phone please."
        except IndexError:
            return "Enter user name."
        except KeyError:
            return "Contact not found!"

    return inner


def parse_input(user_input):
    '''Парсер команд'''
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def add_contact(args, book: AddressBook):
    '''Функція додавання нового запису до адресної книги.'''
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def change_contact(args, book: AddressBook):
    '''Функція збереження нового номеру для контакту із заданим ім'ям.
    Якщо контакт з заданим ім'ям не існує, то користувач отримає
    відповідне повідомлення
    '''
    message = "Contact updated."
    name, old_phone, new_phone, *_ = args
    record = book.find(name)
    if record:
        record.edit_phone(old_phone, new_phone)
    else:
        message = f"Contact with name {name} not found!"
    return message


@input_error
def show_phone(args, book: AddressBook):
    '''Функція повертає телефонні номери для контакту з заданим ім'ям.'''
    return ", ".join(phone.value for phone in book[args[0]].phones)


@input_error
def add_birthday(args, book: AddressBook):
    '''Функція додає дату народження для вказаного контакту.'''
    name, birthday, *_ = args
    record = book.find(name)
    message = "Birthday added."
    if record:
        if record.birthday:
            message = "Birthday updated."
        record.add_birthday(birthday)
    else:
        message = f"Contact with name {name} not found!"
    return message


@input_error
def show_birthday(args, book: AddressBook):
    '''Функція повертає дату народження для вказаного контакту'''
    if book[args[0]].birthday:
        return book[args[0]].birthday.value
    else:
        return f"Birthday for contact with name {args[0]} not found!"


def birthdays(book: AddressBook):
    '''Функція повертає список користувачів, яких потрібно привітати по днях
    на наступному тижні
    '''
    upcoming_birthdays = book.get_upcoming_birthdays()
    return f"{'\n'.join(b['name'] + ": " + b['congratulation_date']
                        for b in upcoming_birthdays)}"

def main():
    '''Функція з реалізованою логікою взаємодії з користувачем'''
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        if not user_input or user_input.isspace():
            print("You didn't enter a command.")
            continue

        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            print(change_contact(args, book))

        elif command == "phone":
            print(show_phone(args, book))

        elif command == "all":
            print(book)

        elif command == "add-birthday":
            print(add_birthday(args, book))

        elif command == "show-birthday":
            print(show_birthday(args, book))

        elif command == "birthdays":
            print(birthdays(book))

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()
