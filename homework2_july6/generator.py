import re
from typing import Callable, Generator

def generator_numbers(text: str) -> Generator[float, None, None]: # Пошук усіх дійсних чисел, відокремлених пробілами
    matches = re.findall(r'(?<=\s)\d+\.\d+(?=\s)', f' {text} ')
    for match in matches:
        yield float(match)

def sum_profit(text: str, func: Callable[[str], Generator[float, None, None]]) -> float: # Функція для підрахунку суми всіх чисел, знайдених у текст
    return sum(func(text))

# Приклад використання
text = "Загальний дохід працівника складається з декількох частин: 1000.01 як основний дохід, доповнений додатковими надходженнями 27.45 і 324.00 доларів."
total_income = sum_profit(text, generator_numbers)
print(f"Загальний дохід: {total_income}")