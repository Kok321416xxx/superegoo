import csv
import re
from collections import Counter

import pandas as pd

file_csv = "../data/transactionscsv.csv"


def file_path_csv(file_path_csv) -> list:
    """
    Функция принимает на вход путь к файлу csv и возвращает список словарей с транзациями
    """
    try:
        with open(file_path_csv, newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file, delimiter=";")
            next(reader)
            rows = list(reader)
            return rows
    except FileNotFoundError:
        print(f"Файл '{file_csv}' не найден.")
        return None
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return None


# print(file_path_csv(file_csv))

file_excel = "../data/transactions_excel.xlsx"


def file_path_exel(file_path_exel):
    """
    Функция принимает на вход путь к файлу exel и возвращает список словарей с транзакциями
    """
    try:
        excel_data = pd.read_excel(file_path_exel, engine="openpyxl")
        transactions = excel_data.to_dict("records")
        return transactions
    except FileNotFoundError:
        print(f"Файл '{file_path_exel}' не найден.")
        return None
    except Exception as e:
        print(f"Произошла ошибка при чтении файла: {e}")
        return None


# print(file_path_exel(file_excel))


def find_transactions(some_dict, str_find):
    """Получает на вход словарь csv или эксель и возвращает список словарей с тем ключевым словом которое вы указалаи в str_find"""
    try:
        pattern = re.compile(str_find, flags=re.IGNORECASE)
        matching_operations = []
        for operation in some_dict:
            description = str(operation.get("description", ""))
            if pattern.search(description):
                matching_operations.append(operation)
        return matching_operations
    except Exception as e:
        print(f"Ошибка {e}")


# print(find_transactions((file_path_csv(file_csv)), "счет"))
# print(find_transactions((file_path_exel(file_excel)), "счет"))

categories = ["Перевод с карты на карту", "Открытие вклада", "Перевод организации", "Перевод со счета на счет"]
o = file_path_csv(file_csv)
e = file_path_exel(file_excel)


# print(e)


def count_operations_by_description(dickt_list_ex_cs_js: list[dict], find_str: str) -> list[dict]:
    """ """
    if not dickt_list_ex_cs_js or not find_str:
        return []
    try:
        pattern = re.compile(find_str, re.IGNORECASE)
    except re.error:
        return []
    finder_dickt = []
    for dick in dickt_list_ex_cs_js:
        if dick.get("description") and pattern.search(dick.get("description")):
            finder_dickt.append(dick)
    return finder_dickt


def count_operations_by_description(operations: list[dict], categories_1: list[str]) -> dict:
    """
    Функция принимает список словарей с данными о банковских операциях и список категорий операций.
    Возвращает словарь, где ключи — это названия категорий, а значения — количество операций в каждой категории.
    Категория определяется по полю 'description'.
    """
    category_counts = Counter()
    descriptions = [trans.get("description", "").lower() for trans in operations]
    for category in categories_1:
        category_lower = category.lower()
        category_counts[category] = sum(1 for desc in descriptions if category_lower in desc)

    return dict(category_counts)

# result = count_operations_by_description(o, categories)
# print(result)
