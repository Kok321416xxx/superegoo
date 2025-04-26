import logging
import os

from src.generators import transactions

log_directory = os.path.join(os.getcwd(), "logs")
os.makedirs(log_directory, exist_ok=True)  # Создаем папку logs, если она еще не существует

# Основная конфигурация logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=os.path.join(log_directory, "application.log"),  # Указываем путь к файлу в папке logs
    filemode="w",  # Перезапись файла при каждом запуске
)
auth_logger_processing = logging.getLogger("app.auth")


def filter_by_state(dict_for_state, state: str = "EXECUTED") -> list[dict]:
    """Принимает список словарей и возвращает словари, у которых ключ state соответствует указанному значению."""
    auth_logger_processing.info("Запуск функции")
    filtered_list = []
    for d in dict_for_state:
        if d.get("state") == state:
            filtered_list.append(d)
    return filtered_list


def sort_by_date(dict_sort_by_date: list[dict], reverse: bool = True) -> list[dict]:
    """Принимает список словарей, возвращает новый список, отсортированный по дате (date)"""
    auth_logger_processing.info("Запуск функции")
    return sorted(dict_sort_by_date, key=lambda x: x.get("date"), reverse=reverse)


print(filter_by_state(transactions))
