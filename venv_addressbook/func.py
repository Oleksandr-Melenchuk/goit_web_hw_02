from decorators import *
from objects import *
import pickle


def save_data(book: AddressBook, filename="addressbook.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(book, f)


def load_data(filename="addressbook.pkl"):
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()


@input_error
def add_contact(args, book: AddressBook):
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
def show_birthday(args, book):
    name = args[0]
    record = book.find(name)
    return f"{name}  birthday: {record.birthday.value}"


@input_error
def birthdays(book):
    return (
        "\n".join(
            [
                f"{item['name']}: {item['birthday']}"
                for item in book.get_upcoming_birthdays()
            ]
        )
        or "No upcoming birthdays."
    )


@input_error
def change_contact(book: AddressBook, args):
    name, old_phone, new_phone = args
    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Contact updated"


@input_error
def show_phone(book: AddressBook, args):
    name = args[0]
    record = book.find(name)
    phones_str = "; ".join(phone.value for phone in record.phones)
    return f"{name}: {phones_str}"


@input_error
def show_all(book: AddressBook):
    return "\n".join(str(record) for record in book.data.values())


@input_error
def add_birthday(args, book):
    name, date = args
    record = book.find(name)
    record.add_birthday(date)
    return "Birthday added."


@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args
