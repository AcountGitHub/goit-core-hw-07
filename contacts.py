
'''Реалізація класів для управління адресною книгою'''

from collections import UserDict
from datetime import datetime, date, timedelta

class Field:
    '''Базовий клас для полів запису.'''
    def __init__(self, value):
        self.value = value


    def __str__(self):
        return str(self.value)


class Name(Field):
    '''Клас для зберігання імені контакту.'''
    pass


class Phone(Field):
    '''Клас для зберігання номера телефону.'''
    def __init__(self, phone_number):
        # Валідація номера телефону, перевірка на 10 цифр
        if len(phone_number) == 10 and phone_number.isdigit():
            super().__init__(phone_number)
        else:
            raise AddressBookValueError("The phone number must contain only 10 digits.")


class Birthday(Field):
    '''Клас для зберігання дня народження.'''
    def __init__(self, value):
        try:
            # Перевірка коректності даних
            # та перетворення рядка на об'єкт datetime
            datetime.strptime(value, "%d.%m.%Y")
        except ValueError:
            raise AddressBookValueError("Invalid date format. Use DD.MM.YYYY")
        super().__init__(value)


class Record:
    '''Клас для зберігання інформації про контакт, включаючи ім'я та список телефонів.'''
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None


    def add_birthday(self, birthday):
        '''Метод додавання дати народження'''
        self.birthday = Birthday(birthday)


    def add_phone(self, phone_number):
        '''Метод додавання номеру телефону'''
        if self.find_phone(phone_number) is None:
            self.phones.append(Phone(phone_number))


    def remove_phone(self, phone_number):
        '''Метод видалення номеру телефону'''
        self.phones = list(filter(lambda p: p.value != phone_number, self.phones))


    def edit_phone(self, old_number, new_number):
        '''Метод редагування номеру телефону'''
        old_phone = self.find_phone(old_number)
        if not old_phone is None:
            old_phone.value = Phone(new_number).value
        else:
            raise AddressBookValueError(f"Phone number {old_number} not found!")


    def find_phone(self, phone_number):
        '''Метод пошуку номеру телефону'''
        result = list(filter(lambda p: p.value == phone_number, self.phones))
        return result[0] if len(result) > 0 else None


    def __str__(self):
        result = f"Contact name: {self.name.value}, phones: {'; '.join(p.value
                                                                for p in self.phones)}"
        if self.birthday:
            result += f", birthday: {self.birthday.value}"
        return result


class AddressBook(UserDict):
    '''Клас для зберігання та управління записами.'''
    def add_record(self, record):
        '''Метод додавання запису до адресної книги'''
        if self.find(record.name.value) is None:
            self.data[record.name.value] = record


    @staticmethod
    def string_to_date(date_string):
        '''Метод перетворює рядок з датою в об'єкт datetime'''
        return datetime.strptime(date_string, "%d.%m.%Y").date()


    @staticmethod
    def adjust_for_weekend(birthday):
        '''Якщо дата народження випадає на вихідний, метод повертає
        дату наступного понеділка
        '''
        if birthday.weekday() >= 5:
            return AddressBook.find_next_weekday(birthday, 0)
        return birthday


    @staticmethod
    def find_next_weekday(start_date, weekday):
        '''Метод дозволяє знайти дату наступного конкретного дня тижня
        після заданої дати
        '''
        days_ahead = weekday - start_date.weekday()
        if days_ahead <= 0:
            days_ahead += 7
        return start_date + timedelta(days=days_ahead)


    def get_upcoming_birthdays(self, days=7):
        '''Метод визначає контакти, у яких день народження припадає
        вперед на 7 днів включаючи поточний день.
        '''
        upcoming_birthdays = []
        today = date.today()

        for name in self.data:
            if self.data[name].birthday:
                birthday_this_year = \
                    AddressBook.string_to_date(
                        self.data[name].birthday.value).replace(year=today.year)
                # Перевірка, чи не буде
                # припадати день народження вже наступного року.
                if birthday_this_year < today:
                    birthday_this_year = \
                        AddressBook.string_to_date(
                            self.data[name].birthday.value).replace(year=today.year+1)

                if 0 <= (birthday_this_year - today).days <= days:
                    # Перенесення дати привітання на наступний робочий день,
                    # якщо день народження припадає на вихідний.
                    birthday_this_year = AddressBook.adjust_for_weekend(birthday_this_year)

                    congratulation_date_str = birthday_this_year.strftime("%d.%m.%Y")
                    upcoming_birthdays.append({
                        "name": self.data[name].name.value,   
                        "congratulation_date": congratulation_date_str
                        })
        return upcoming_birthdays


    def find(self, name):
        '''Метод пошуку запису за ім'ям'''
        return self.data.get(name)


    def delete(self, name):
        '''Метод видалення запису за ім'ям'''
        self.data = {key: self.data[key] for key in self.data if key != name}


    def __str__(self):
        return f"{'\n'.join(self.data[k].__str__() for k in self.data)}"


class AddressBookValueError(ValueError):
    '''Клас винятку для адресної книги'''
    pass
