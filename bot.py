from classes import Record, AddressBook
import json
import os

class InputError(Exception):
    pass

class ContactAssistant:
    
    YLLOW_TEXT = "\033[33m"
    GREEN_TEXT = "\033[32m"
    RED_TEXT = "\033[31m"
    DEFALUT_TEXT = "\033[0m"
    PURPURE_TEXT = "\033[35m"
    BIRUZA_TEXT = "\033[36m"
    LIST_COMANDS_BOT = ["hello", "add", "change","phone","show all",'search',"good bye", "close", "exit"]
    DOSTUPNI_COMANDY = f"{RED_TEXT}Доступні наступні команди : {GREEN_TEXT}{LIST_COMANDS_BOT}{DEFALUT_TEXT}"
    PISKAZKA_SHOW_ALL = f"\nКоманда - {GREEN_TEXT}show all{YLLOW_TEXT} - покаже доступні контакти{DEFALUT_TEXT}"
    
    def __init__(self):
        self.address_book = AddressBook()
        self.file_path = "contacts.json"
       
        if os.path.exists(self.file_path):
            self.load_data()

    def save_data(self):
        with open(self.file_path, "w") as file:
            data = {
                "records": [record.__json__() for record in self.address_book.values()]
            }
            json.dump(data, file)

    def load_data(self):
        try:
            if os.path.getsize(self.file_path) > 0:  
                with open(self.file_path, "r") as file:
                    data = json.load(file)
                    records = [Record(record["name"], record.get("birthday")) for record in data.get("records", [])]
                    for i, record in enumerate(records):
                        if "phones" in data.get("records", [])[i]:
                            for phone in data["records"][i]["phones"]:
                                record.add_phone(phone)
                        self.address_book.add_record(record)
        except (OSError, json.JSONDecodeError, KeyError) as e:
            print(f"Error loading data: {e}")


    def add_contact(self, name, phone, birthday=None):
        try:
            record = Record(name, birthday)
            record.add_phone(str(phone).strip()) 
            self.address_book.add_record(record)
            self.save_data()
            return  f"{self.YLLOW_TEXT}Новий контакт успішно додано!!!{self.PISKAZKA_SHOW_ALL}"
        except ValueError as e:
            raise InputError(str(e))

    def change_contact(self, name, phone):
        try:
            record = self.address_book.find(name)
            if record :
                if len(phone) == 10 and phone.isdigit():
                    print(phone)
                    record.phones = []  
                    record.add_phone(phone)
                    self.save_data()  
                    return f"{self.YLLOW_TEXT}Номер телефону успішно змінено!!!{self.PISKAZKA_SHOW_ALL}"
                else:
                    raise ValueError(f"{self.YLLOW_TEXT}Номер може містити тільки 10 цифри !!!{self.BIRUZA_TEXT}\n# Приклад - 0931245891")
            else:
                raise IndexError(f"{self.YLLOW_TEXT}Такого іменні не знайдено у вашій телефоній книзі !!!{self.DEFALUT_TEXT}{self.PISKAZKA_SHOW_ALL} ")
        except (ValueError, IndexError) as e:
            raise InputError(str(e))

    def get_phone(self, name):
        try:
            record = self.address_book.find(name)
            if record:
                return f"{self.YLLOW_TEXT}За вказаним іменем {self.BIRUZA_TEXT}{name}{self.YLLOW_TEXT} знайдено номер{self.BIRUZA_TEXT} {record.phones[0]}{self.DEFALUT_TEXT}"
            else:
                raise IndexError(f"{self.YLLOW_TEXT}Такого іменні не знайдено у вашій телефоній книзі !!!{self.DEFALUT_TEXT}{self.PISKAZKA_SHOW_ALL} ")
        except (ValueError, IndexError) as e:
            raise InputError(str(e))

    def show_all_contacts(self):
        records = list(self.address_book.values())
        if not records:
            return f"{self.YLLOW_TEXT}Ваша телефона книга поки не містить жодного запису{self.DEFALUT_TEXT}"
        else:
            result = f'{self.GREEN_TEXT}{"Name":<10}  {"Phone":<12}{self.YLLOW_TEXT}\n'
            for record in records:
                phone_numbers = ', '.join(str(phone) for phone in record.phones)
                result += f"{f"{record.name}":<10} {phone_numbers}\n" 
            return result.strip()


class CommandHandler:
    YLLOW_TEXT = "\033[33m"
    GREEN_TEXT = "\033[32m"
    RED_TEXT = "\033[31m"
    DEFALUT_TEXT = "\033[0m"
    PURPURE_TEXT = "\033[35m"
    BIRUZA_TEXT = "\033[36m"
    LIST_COMANDS_BOT = ["hello", "add", "change","phone","show all",'search',"good bye", "close", "exit"]
    DOSTUPNI_COMANDY = f"{RED_TEXT}Доступні наступні команди : {GREEN_TEXT}{LIST_COMANDS_BOT}{DEFALUT_TEXT}"
    BAD_COMMAND_ADD = f"{YLLOW_TEXT}Невірні параметри для команди {GREEN_TEXT}add{YLLOW_TEXT} !!!.\n\
                        {RED_TEXT}# Приклад {GREEN_TEXT}add{BIRUZA_TEXT} Імя_контакту{YLLOW_TEXT} Номер_телефону {DEFALUT_TEXT}"
    
    BAD_COMMAND_CHANGE = f"{YLLOW_TEXT}Невірні параметри для команди {GREEN_TEXT}change{YLLOW_TEXT} !!!.\n\
                           {RED_TEXT}# Приклад {GREEN_TEXT}change{BIRUZA_TEXT} Імя_контакту{YLLOW_TEXT} "
    
    BAD_COMMAND_PHONE = f"{YLLOW_TEXT}Невірні параметри для команди {GREEN_TEXT}phone{YLLOW_TEXT} !!!.\n\
                           {RED_TEXT}# Приклад {GREEN_TEXT}phone{BIRUZA_TEXT} Імя_контакту{YLLOW_TEXT} "
    
    BAD_COMMAND_SEARCH = f"{YLLOW_TEXT}Невірні параметри для команди {GREEN_TEXT}search{YLLOW_TEXT} !!!.\n\
                           {RED_TEXT}# Приклад {GREEN_TEXT}search{BIRUZA_TEXT} Імя_контакту{YLLOW_TEXT} "
    
    
    def __init__(self, contact_assistant):
        self.contact_assistant = contact_assistant

    def handle_hello(self, args):
        return f"{self.YLLOW_TEXT}How can I help you?{self.DEFALUT_TEXT}"

    def handle_add(self, args):
        if len(args) == 0:
            raise InputError(self.BAD_COMMAND_ADD)

        contact_info = args.split(" ")
        if len(contact_info) != 3:
            raise InputError(self.BAD_COMMAND_ADD)

        _, name, phone = args.split(" ")
        return self.contact_assistant.add_contact(name, phone)

    def handle_change(self, args):
        if len(args) == 0:
            raise InputError(self.BAD_COMMAND_CHANGE)

        contact_info = args.split(" ")
        if len(contact_info) != 3:
            raise InputError(self.BAD_COMMAND_CHANGE)

        _, name, phone = args.split(" ")
        return self.contact_assistant.change_contact(name, phone)

    def handle_phone(self, args):
        if len(args) == 0:
            raise InputError(self.BAD_COMMAND_PHONE)
        args_list = args.split(" ")
        name = args_list[1]
        return self.contact_assistant.get_phone(name)

    def handle_show(self, args):
        return self.contact_assistant.show_all_contacts()

    def handle_bye(self, args):
        print("Good bye!")
        return None
    
    def handle_search(self, args):
        if len(args) == 0:
            raise InputError(self.BAD_COMMAND_SEARCH)

        query = args.split(" ", 1)[1]
        matching_records = self.contact_assistant.address_book.search(query)

        if not matching_records:
            return f"{self.YLLOW_TEXT}Нажаль нічого не знайдено  {self.DEFALUT_TEXT}"
        else:
            result = f"{self.YLLOW_TEXT}За Вашим запитом = {self.RED_TEXT}{query}{self.YLLOW_TEXT} було знайдено наступні записи :{self.DEFALUT_TEXT}\n"
            for record in matching_records:
                phone_numbers = ', '.join(str(phone) for phone in record.phones)
                result += f"{record.name}: {phone_numbers}\n"
            return result.strip()

    def choice_action(self, data):
        actions = {
            'hello': self.handle_hello,
            'add': self.handle_add,
            "change": self.handle_change,
            "phone": self.handle_phone,
            'search': self.handle_search,
            "show": self.handle_show,
            "close": self.handle_bye,
            "exit": self.handle_bye,
            "good bye": self.handle_bye,
        }
        return actions.get(data, lambda args: f'{self.YLLOW_TEXT}Tака команда не пітримується наразі\n{self.DEFALUT_TEXT}{self.DOSTUPNI_COMANDY}')

    def process_input(self, user_input):
        try:
            if not user_input:
                raise InputError(f'{self.YLLOW_TEXT}Ви нічого не ввели \n{self.DOSTUPNI_COMANDY}')

            space_index = user_input.find(' ')

            if space_index != -1:
                first_word = user_input[:space_index]
            else:
                first_word = user_input

            if first_word in ["good", "bye"]:
                first_word = "good bye"

            func = self.choice_action(first_word)
            result = func(user_input)

            if result is None:
                return None
            else:
                return result
        except InputError as e:
            return str(e)

class Bot:
    YLLOW_TEXT = "\033[33m"
    GREEN_TEXT = "\033[32m"
    RED_TEXT = "\033[31m"
    DEFALUT_TEXT = "\033[0m"
    PURPURE_TEXT = "\033[35m"
    BIRUZA_TEXT = "\033[36m"
    LIST_COMANDS_BOT = ["hello", "add", "change","phone","show all",'search',"good bye", "close", "exit"]
    print(f'\n{YLLOW_TEXT}Вас вітає Бот для роботи з вашии контактами.')
    print(f'{RED_TEXT}Доступні наступні команди : {GREEN_TEXT}{LIST_COMANDS_BOT}{DEFALUT_TEXT}')
    
    def run(self):
        contact_assistant = ContactAssistant()
        command_handler = CommandHandler(contact_assistant)

        while True:
            try:
                user_input = input(f"{self.PURPURE_TEXT}ВВедіть команду>>{self.DEFALUT_TEXT}").lower().strip()
                result = command_handler.process_input(user_input)

                if result is None:
                    break
                else:
                    print(result)

            except Exception as e:
                print(e)


