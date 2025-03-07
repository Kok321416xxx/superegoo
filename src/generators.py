transactions = [
    {
        "id": 939719570,
        "state": "EXECUTED",
        "date": "2018-06-30T02:08:58.425572",
        "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод организации",
        "from": "Счет 75106830613657916952",
        "to": "Счет 11776614605963066702",
    },
    {
        "id": 142264268,
        "state": "EXECUTED",
        "date": "2019-04-04T23:20:05.206878",
        "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
        "description": "Перевод со счета на счет",
        "from": "Счет 19708645243227258542",
        "to": "Счет 75651667383060284188",
    },
]


# 1 задача
def filter_by_currency(transactions):
    for t in transactions:
        if t["operationAmount"]["currency"]["code"] == "USD":
            yield t


# пример по которому должная работать функция
usd_transactions = filter_by_currency(transactions)
try:
    for _ in range(5):
        print(next(usd_transactions))
except StopIteration:
    print("Список транзакций пуст")


# 2 задача
def transaction_descriptions(transactions):
    for transaction in transactions:
        yield transaction.get("description")


descriptions = transaction_descriptions(transactions)
for _ in range(2):
    print(next(descriptions))


# 3 задача
def card_number_generator(start, stop):
    for numbers in range(start, stop + 1):
        formated_numbers = f"{numbers:0>16}"
        yield formated_numbers[:4] + " " + formated_numbers[4:8] + " " + formated_numbers[
            8:12
        ] + " " + formated_numbers[12:]


for card_number in card_number_generator(1, 5):
    print(card_number)
