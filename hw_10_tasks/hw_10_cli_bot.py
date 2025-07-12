import pickle #added as HW12

from hw_06_classes import AddressBook, Record
from functools import wraps
from hw_04_birthdays import get_upcoming_birthdays

# ======= Serialization / Deserialization =======
def save_data(book, filename="addressbook.pkl"):  #added as HW12
    with open(filename, "wb") as f:
        pickle.dump(book, f)

def load_data(filename="addressbook.pkl"): #added as HW12
    try:
        with open(filename, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        return AddressBook()

# ======= Decorator =======
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

# ======= Parser =======
def parse_input(user_input):
    parts = user_input.strip().split()
    if not parts:
        return "", []
    cmd = parts[0].lower()
    args = parts[1:]
    return cmd, args

# ======= Command Handler =======
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

@input_error
def birthdays(args, book: AddressBook):
    users = []
    for record in book.data.values():
        if record.birthday:
            users.append({
                "name": record.name.value,
                "birthday": record.birthday.value.strftime("%Y.%m.%d")
            })
    upcoming = get_upcoming_birthdays(users)
    if not upcoming:
        return "No upcoming birthdays this week."
    return "\n".join(f"{b['name']} → {b['congratulation_date']}" for b in upcoming)

@input_error
def add_birthday(args, book: AddressBook): #Додати дату народження для вказаного контакту.
    if len(args) != 2:
        raise ValueError("Enter name and birthday in format DD.MM.YYYY")
    
    name, bday = args
    record = book.find(name)
    if not record:
        record = Record(name)
        book.add_record(record)
    record.add_birthday(bday)
    return f"Birthday added for {name}."

@input_error
def show_birthday(args, book: AddressBook): #Показати дату народження для вказаного контакту.
    if len(args) != 1:
        raise ValueError("Enter the name to show birthday.")
    
    name = args[0]
    record = book.find(name)
    if not record:
        raise KeyError("Contact not found.")
    if not record.birthday:
        return "Birthday not set for this contact."
    return f"{name}'s birthday is {record.birthday}"


# ======= Main Function ======= 
def main():
    book = load_data()  # added as HW12 - Load existing data or create a new AddressBook instance 
    print("Welcome to the assistant bot!")

    while True:
        user_input = input("Enter a command: ")
        command, args = parse_input(user_input)

        if command in ["exit", "close"]:
            save_data(book) # added as HW12 - Save data before exiting
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
        elif command == "birthdays":
            print(birthdays(args, book))
        elif command == "add-birthday":
            print(add_birthday(args, book))
        elif command == "show-birthday":
            print(show_birthday(args, book))
        else:
            print("Invalid command.")
       

if __name__ == "__main__":
    main()