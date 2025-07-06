def caching_fibonacci():
    cache = {} #Створюємо порожній словник, який буде доступний внутрішній функції fibonacci завдяки замиканню

    def fibonacci(n):
        if n <= 0: # Базові випадки для ряду Фібоначчі
            return 0
        elif n == 1: # Базові випадки для ряду Фібоначчі
            return 1
        if n in cache: # Перевіряємо, чи число вже є в кеші. Якщо так, повертаємо його без додаткових обчислень.
            return cache[n]
        cache[n] = fibonacci(n - 1) + fibonacci(n - 2) # Якщо числа немає в кеші, обчислюємо його рекурсивно. Результат зберігаємо в кеші перед тим, як повернути.
        return cache[n]

    return fibonacci # Повертаємо внутрішню функцію fibonacci, яка "пам'ятає" словник cache

fib = caching_fibonacci() # Отримуємо функцію fibonacci

print(fib(10))  # Виведе 55
print(fib(15))  # Виведе 610