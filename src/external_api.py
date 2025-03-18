import os

import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("EXCHANGE_RATES_API_KEY")
URL = os.getenv("url")

empty_dict = {}


def get_transaction_amount_in_rubles(transaction: float) -> float:
    """Функция обрабатывает, транзацию или серию транзаций и передает дальше в функцию convert_currency
    на перевод в другую валюту если она не соответсвует требованиям
    """
    amount = transaction.get("operationAmount", {"amount": 0})["amount"]
    currency = transaction.get("operationAmount", {"currency": {"code": "RUB"}})["currency"]["code"]
    if currency == "RUB":
        return amount
    elif currency in ("USD", "EUR"):
        return convert_currency(amount, currency)
    else:
        raise ValueError(f"Неподдерживаемая валюта: {currency}")


def convert_currency(amount: str, from_curency: str) -> float:
    """
    Функция для конвертации суммы из одной валюты в другую через API
    нужно было делать через try и exept, но как успел, может потом переделаю
    """
    headers = {"apikey": API_KEY}
    response = requests.get(URL.format(to="RUB", fromm_v=from_curency, amount=amount), headers=headers)
    if response.status_code == 200:
        data = response.json()
        rate = data["result"]
        return float(rate)


transaction = {
    "id": 414894334,
    "state": "EXECUTED",
    "date": "2019-06-30T15:11:53.136004",
    "operationAmount": {"amount": "95860.47", "currency": {"name": "руб.", "code": "USD"}},
    "description": "Перевод со счета на счет",
    "from": "Счет 59956820797131895975",
    "to": "Счет 43475624104328495820",
}
print(get_transaction_amount_in_rubles(transaction))
