from datetime import datetime
from collections import UserDict

class Field:
    def __init__(self, value):
        if not self.is_valid(value):
            if f"{self.__class__.__name__.lower()}" == "phone" :
        
                raise ValueError(f"Номер може містити тільки 10 цифри !!!\n# Приклад - 0931245891")
        self.__value = value

    @property
    def value(self):
        return self.__value

    @value.setter
    def value(self, new_value):
        if not self.is_valid(new_value):
            if f"{self.__class__.__name__.lower()}" == "phone" :
        
                raise ValueError(f"Номер може містити тільки 10 цифри !!!\n# Приклад - 0931245891")
        self.__value = new_value

    def __str__(self):
        return str(self.value)

    def is_valid(self, value):
        return isinstance(value, (int, float, str))
    
    def __json__(self):
        return self.value


class Name(Field):
    pass


class Phone(Field):
    def is_valid(self, value):
        if  (len(value) == 10 and value.isdigit()):
            return value
        else :
            raise ValueError(f"Invalid phone number format phone for '{value}'")

class Birthday(Field):
    def is_valid(self, value):        
        try:
            datetime.strptime(value, "%Y-%m-%d")
            return True
        except ValueError:
            return False


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        phone_obj = Phone(phone)
        self.phones.append(phone_obj)

    def remove_phone(self, phone):
        initial_len = len(self.phones)
        self.phones = [p for p in self.phones if p.value != phone]
        if len(self.phones) == initial_len:
            raise ValueError(f"Phone number '{phone}' not found")

    def edit_phone(self, old_phone, new_phone):
        if not Phone(new_phone).is_valid(new_phone):
            raise ValueError(f"Invalid phone number format for '{new_phone}'")
        for p in self.phones:
            if p.value == old_phone:
                p.value = new_phone
                return
        raise ValueError(f"Phone number '{old_phone}' not found")

    def find_phone(self, phone):
        found_numbers = [p for p in self.phones if p.value == phone]
        return found_numbers[0] if found_numbers else None

    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            birthday_date = datetime.strptime(self.birthday.value, "%Y-%m-%d").date()

            next_birthday = datetime(today.year, birthday_date.month, birthday_date.day).date()
            if today > next_birthday:
                next_birthday = datetime(today.year + 1, birthday_date.month, birthday_date.day).date()

            days_left = (next_birthday - today).days
            return days_left
        else:
            return None
        
    def __json__(self):
        record_data = {
            "name": self.name.__json__(),
            "phones": [phone.__json__() for phone in self.phones],
            "birthday": self.birthday.__json__() if self.birthday else None
        }
        return record_data

class AddressBook(UserDict):
    def search(self, query):
        matching_records = []

        for record in self.data.values():
            if query.lower() in record.name.value.lower():
                matching_records.append(record)
            for phone in record.phones:
                if query in str(phone.value):
                    matching_records.append(record)

        return matching_records
    
    def add_record(self, record):
        self.data[record.name.value] = record
   
    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self, page_size=10):
        keys = list(self.data.keys())
        for i in range(0, len(keys), page_size):
            yield [self.data[key] for key in keys[i:i + page_size]]

    def find(self, name):
        return self.data.get(name)