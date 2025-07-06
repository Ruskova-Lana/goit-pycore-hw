from hw_06_classes import AddressBook, Record
from hw_04_users import users


if __name__ == "__main__":
    # Створення нової адресної книги
    book = AddressBook()

    # Додавання користувачів із users_data.py
    for user in users:
        record = Record(user["name"])
        record.add_birthday(user["birthday"])  # формат: "DD.MM.YYYY"
        record.add_phone("0500000000")  # Можна додати умовний номер
        book.add_record(record)

    # Додатково: ручне створення запису для John з кількома телефонами
    john_record = Record("John")
    john_record.add_phone("1234567890")
    john_record.add_phone("5555555555")
    john_record.add_birthday("05.07.1985")
    book.add_record(john_record)

    # Додатковий запис для Jane
    jane_record = Record("Jane")
    jane_record.add_phone("9876543210")
    jane_record.add_birthday("07.07.1990")
    book.add_record(jane_record)

    # Виведення всіх записів
    print("=== Усі записи в адресній книзі ===")
    for name, record in book.data.items():
        print(record)

    # Знаходження та редагування телефону для John
    john = book.find("John")
    john.edit_phone("1234567890", "1112223333")
    print("\n=== Оновлений запис John ===")
    print(john)  # Виведення: Contact name: John, phones: 1112223333; 5555555555

    # Пошук конкретного телефону у записі John
    found_phone = john.find_phone("5555555555")
    print(f"\nPhone found for {john.name.value}: {found_phone}")

    # Видалення запису Jane
    book.delete("Jane")

    # Виведення всіх записів після видалення
    print("\n=== Після видалення Jane ===")
    for name, record in book.data.items():
        print(record)

    # Отримання та виведення майбутніх привітань
    print("\n=== Привітання на наступному тижні ===")
    birthdays = book.get_birthdays_for_next_week()
    if birthdays:
        for b in birthdays:
            print(f"{b['name']} → {b['congratulation_date']}")
    else:
        print("Немає днів народження на наступному тижні.")
