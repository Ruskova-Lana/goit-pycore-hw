from hw_06_classes import AddressBook, Record
from functools import wraps

def input_error(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except (ValueError, IndexError):
            return "Enter the argument for the command"
    return wrapper

def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args

@input_error
def add_contact(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError
    name, phone = args
    record = book.find(name)
    if record:
        record.add_phone(phone)
    else:
        record = Record(name)
        record.add_phone(phone)
        book.add_record(record)
    return "Contact added."

@input_error
def change_contact(args, book: AddressBook):
    if len(args) != 2:
        raise ValueError
    name, new_phone = args
    record = book.find(name)
    if not record:
        raise KeyError
    if record.phones:
        old_phone = record.phones[0].value
        record.edit_phone(old_phone, new_phone)
    else:
        record.add_phone(new_phone)
    return "Contact updated."

@input_error
def show_phone(args, book: AddressBook):
    if len(args) != 1:
        raise IndexError
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError
    if not record.phones:
        return "No phone numbers found for this contact."
    phones = "; ".join(phone.value for phone in record.phones)
    return phones

def show_all(book: AddressBook):
    if not book.data:
        return "No contacts saved."
    result = []
    for record in book.data.values():
        phones = "; ".join(phone.value for phone in record.phones)
        result.append(f"{record.name.value}: {phones}")
    return "\n".join(result)

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["exit", "close"]:
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
            print(show_all(book))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()