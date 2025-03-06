import pytest
from src.masks import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date
from src.generators import card_number_generator, transaction_descriptions
from src.decorators import log


def test_assert_get_mask_card_number(fixture_get_mask_card_number):
    """Тест функции get_mask_card_number"""
    for num_card, expected_mask in fixture_get_mask_card_number:
        assert get_mask_card_number(num_card) == expected_mask


def test_get_mask_account(fixture_get_mask_account):
    """тест функции get_mask_account"""
    for num_card, expected_mask in fixture_get_mask_account:
        assert get_mask_account(num_card) == expected_mask


@pytest.mark.parametrize(
    "arg, expected_result",
    [
        ("Visa Platinum 1234567890123456", "Visa Platinum 1234 56** **** 3456"),
        ("Счет 12345678901234567890", "Счет **7890"),
        ("Maestro 1234567890123456", "Maestro 1234 56** **** 3456"),
        ("Maestro 1596837868705199", "Maestro 1596 83** **** 5199"),
        ("Счет 64686473678894779589", "Счет **9589"),
        ("MasterCard 7158300734726758", "MasterCard 7158 30** **** 6758"),
        ("Счет 35383033474447895560", "Счет **5560"),
        ("Visa Classic 6831982476737658", "Visa Classic 6831 98** **** 7658"),
        ("Visa Platinum 8990922113665229", "Visa Platinum 8990 92** **** 5229"),
        ("Visa Gold 5999414228426353", "Visa Gold 5999 41** **** 6353"),
        ("Счет 73654108430135874305", "Счет **4305"),
    ],
)
def test_mask_account_card(arg, expected_result):
    """Тест функции test_mask_account_card с разными типами входных данных"""
    assert mask_account_card(arg) == expected_result


def test_get_date():
    """Проверка стандартного формата
    Проверка даты с минимальными значениями
    Проверка даты с максимальными значениями
    Проверка даты с одним символом в дне и месяце
    Проверка на пустую строку"""
    assert get_date("2024-03-11T02:26:18.671407") == "11.03.2024"
    assert get_date("0001-01-01T00:00:00.000000") == "01.01.0001"
    assert get_date("9999-12-31T23:59:59.999999") == "31.12.9999"
    assert get_date("2024-01-01T00:00:00.000000") == "01.01.2024"
    with pytest.raises(ValueError):
        get_date("")
    # Проверка на строку без даты
    with pytest.raises(ValueError):
        get_date("T02:26:18.671407")


# Параметризация для функции filter_by_state
@pytest.mark.parametrize(
    "input_data, state, expected_output",
    [
        # Тест 1: Фильтрация по умолчанию (статус 'EXECUTED')
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            "EXECUTED",  # Статус для фильтрации
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
            ],
        ),
        # Тест 2: Фильтрация по статусу 'CANCELED'
        (
            [
                {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
                {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
            "CANCELED",  # Статус для фильтрации
            [
                {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
                {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            ],
        ),
    ],
)
def test_filter_by_state_parametrized(input_data, state, expected_output):
    filtered_data = filter_by_state(input_data, state)
    assert filtered_data == expected_output


def test_sorted_date(sample_data):
    expected_result = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]
    actual_result = sort_by_date(sample_data)
    assert actual_result == expected_result


@pytest.mark.parametrize(
    "start, end, expected", [(1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"])]
)
def test_card_number_generator(start, end, expected):
    assert list(card_number_generator(start, end)) == expected


@pytest.mark.parametrize("expected", [["Перевод организации", "Перевод со счета на счет"]])
def test_transaction_descriptions(transactions, expected):
    assert list(transaction_descriptions(transactions)) == expected


@pytest.mark.parametrize(
    "transaction, expected",
    [
        (
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
                "id": 939719570,
                "state": "EXECUTED",
                "date": "2018-06-30T02:08:58.425572",
                "operationAmount": {"amount": "9824.07", "currency": {"name": "USD", "code": "USD"}},
                "description": "Перевод организации",
                "from": "Счет 75106830613657916952",
                "to": "Счет 11776614605963066702",
            },
        ),
        (
            {
                "id": 142264268,
                "state": "EXECUTED",
                "date": "2019-04-04T23:20:05.206878",
                "operationAmount": {"amount": "79114.93", "currency": {"name": "USD", "code": "USD"}},
                "description": "Перевод со счета на счет",
                "from": "Счет 19708645243227258542",
                "to": "Счет 75651667383060284188",
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
        ),
    ],
)
def test_transaction(transaction, expected):
    assert transaction == expected


def test_log_decorator_err(capsys):
    @log()
    def simpl_add(x, y):
        return x + y

    with pytest.raises(TypeError):
        simpl_add(1, "2")
    masage = capsys.readouterr()
    assert "simpl_add, TypeError, (1, '2'), {} not ok\n" in masage.out


def test_log_decorator(capsys):
    @log()
    def simpl_add(x, y):
        return x + y

    simpl_add(1, 2)
    masage = capsys.readouterr()
    assert "simpl_add status ok\n" in masage.out


def test_open_file():
    @log(filename="log_test_file.txt")
    def simpl_add(x, y):
        return x + y
    simpl_add(1, 2)
    with open("log_test_file.txt", "r", encoding="utf-8") as file:
        lines = file.readlines()
        massage = lines[-1]
        assert massage == "simpl_add status ok\n"


def test_open_file_not_ok():
    with pytest.raises(TypeError):
        @log(filename="log_test_file.txt")
        def simpl_add(x, y):
            return x + y
        simpl_add(1, "2")
        with open("log_test_file.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            massage = lines[-1]
            assert massage == "simpl_add, TypeError, (1, '2'), {} not ok"
