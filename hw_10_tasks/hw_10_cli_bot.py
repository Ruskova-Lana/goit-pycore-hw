from hw_06_classes import AddressBook, Record
from functools import wraps


def input_error(func): # Decorator to handle input errors
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "Contact not found."
        except ValueError as e:
            return str(e)  
        except IndexError:
            return "Enter the argument for the command"
    return wrapper

def parse_input(user_input): # Function to parse user input into command and arguments
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args


@input_error # Function to add or update a contact in the address book
def add_contact(args, book: AddressBook):
    name, *phones = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    for phone in phones:
        if phone:
            record.add_phone(phone)
    return message


@input_error # Function to change a contact's phone number in the address book
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

@input_error # Function to show a contact's phone number
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

def show_all(book: AddressBook): # Function to show all contacts in the address book 
    if not book.data:
        return "No contacts saved."
    result = []
    for record in book.data.values():
        phones = "; ".join(phone.value for phone in record.phones)
        result.append(f"{record.name.value}: {phones}")
    return "\n".join(result)

def main(): # Main function to run the command-line interface bot
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