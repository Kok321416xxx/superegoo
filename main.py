# print(get_mask_card_number("1234567890123456"))
# print(get_mask_account("73654108430135874305"))
# print(mask_account_card("Счет 73654108430135874305"))
# print(get_date("2024-03-11T02:26:18.671407"))
#
# print(
#     sort_by_date(
#         [
#             {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
#             {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
#             {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
#             {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
#         ]
#     )
# )
# print(
#     filter_by_state(
#         [
#             {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
#             {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
#             {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
#             {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
#         ]
#     )
# )
from src.external_api import convert_currency
from src.generators import transaction_descriptions
from src.processing import filter_by_state, sort_by_date
from src.reader_csv_exel_file import file_path_csv, file_path_exel
from src.utils import fin_transaction


def main_logic():
    print("Программа: Привет! Добро пожаловать в программу работы с банковскими транзакциями. ")
    print(
        (
            "Выберите необходимый пункт меню:\n1. Получить информацию о транзакциях из JSON-файла\n2. Получить информацию о транзакциях из CSV-файла\n3. Получить информацию о транзакциях из XLSX-файла"
        )
    )
    s = input()
    if s == "1":
        object_data = fin_transaction("data/operations.json")
        print(object_data)
    elif s == "2":
        object_data = file_path_csv("data/transactionscsv.csv")
        print(object_data)
    elif s == "3":
        object_data = file_path_exel("data/transactions_excel.xlsx")
        print(object_data)
    else:
        print(f"НЕТ ТАКОГО")
    print(
        "Введите статус, по которому необходимо выполнить фильтрацию.\nДоступные для фильтровки статусы: EXECUTED, CANCELED, PENDING"
    )

    user_status = input().lower()
    statuses = ["executed", "canceled", "pending"]
    if user_status in statuses:
        object_data = filter_by_state(object_data, user_status)
    else:
        print(f"Статус операции {user_status} недоступен. Попробуйте ещё раз.")
    print(f"Операции отфильтрованы по статусу {user_status}")

    print("Отсортировать операции по дате? Да/Нет")
    user_date = input()
    if user_date.lower() == "да":
        object_data = sort_by_date(object_data)

    print("Отсортировать по возрастанию или по убыванию? ")
    user_sort = input()
    if user_sort.lower() == "по убыванию":
        object_data = sort_by_date(object_data)
    if user_sort.lower() == "по возрастанию":
        object_data = sort_by_date(object_data, reverse=False)

    print(" Выводить только рублевые тразакции? Да/Нет")
    user_amount = input().lower()
    if user_amount == "да":
        object_data = convert_currency(object_data, "RUB")

    print("Программа: Отфильтровать список транзакций по определенному слову в описании? Да/Нет")
    user_description = input().lower()
    if user_description == "да":
        object_data = transaction_descriptions(object_data)
        print(f"Программа: Распечатываю итоговый список транзакций {list(object_data)}")
    else:
        print(f"Программа: Распечатываю итоговый список транзакций {object_data}")

    print(f"Всего банковских операций в выборке ")


if __name__ == "__main__":
    main_logic()
