import sys
from collections import defaultdict
from typing import List, Dict

def parse_log_line(line: str) -> dict:
    """Парсить рядок лог-файлу у словник."""
    parts = line.strip().split(' ', 3)
    if len(parts) < 4:
        return {}
    return {
        'date': parts[0],
        'time': parts[1],
        'level': parts[2].upper(),
        'message': parts[3]
    }

def load_logs(file_path: str) -> List[dict]:
    """Завантажує лог-файл і повертає список записів."""
    logs = []
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            logs = list(filter(lambda x: x, [parse_log_line(line) for line in f]))
    except FileNotFoundError:
        print(f"Файл не знайдено: {file_path}")
        sys.exit(1)
    except Exception as e:
        print(f"Помилка при читанні файлу: {e}")
        sys.exit(1)
    return logs

def count_logs_by_level(logs: List[dict]) -> Dict[str, int]:
    """Підраховує кількість записів за рівнем логування."""
    counts = defaultdict(int)
    for log in logs:
        counts[log['level']] += 1
    return dict(counts)

def filter_logs_by_level(logs: List[dict], level: str) -> List[dict]:
    """Фільтрує записи за певним рівнем логування."""
    return list(filter(lambda log: log['level'] == level.upper(), logs))

def display_log_counts(counts: Dict[str, int]):
    """Виводить таблицю з кількістю записів."""
    print("\nРівень логування | Кількість")
    print("-----------------|----------")
    for level in sorted(counts.keys()):
        print(f"{level:<16} | {counts[level]}")

def display_filtered_logs(logs: List[dict], level: str):
    """Виводить деталі логів для певного рівня."""
    if logs:
        print(f"\nДеталі логів для рівня '{level.upper()}':")
        for log in logs:
            print(f"{log['date']} {log['time']} - {log['message']}")
    else:
        print(f"\nНемає записів для рівня '{level.upper()}'.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Використання: python main.py path/to/logfile.log [log_level]")
        sys.exit(1)

    log_file_path = sys.argv[1]
    filter_level = sys.argv[2] if len(sys.argv) > 2 else None

    logs = load_logs(log_file_path)
    counts = count_logs_by_level(logs)
    display_log_counts(counts)

    if filter_level:
        filtered_logs = filter_logs_by_level(logs, filter_level)
        display_filtered_logs(filtered_logs, filter_level)