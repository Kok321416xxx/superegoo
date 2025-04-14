from pathlib import Path
from unittest import mock
from unittest.mock import mock_open
from unittest.mock import patch

import pandas as pd
import pytest

from src.decorators import log
from src.external_api import convert_currency
from src.generators import card_number_generator, transaction_descriptions
from src.masks import get_mask_card_number, get_mask_account
from src.processing import filter_by_state, sort_by_date
from src.reader_csv_exel_file import file_path_csv, file_path_exel
from src.utils import fin_transaction
from src.widget import mask_account_card, get_date


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


def test_conver_currency():
    with mock.patch("src.external_api.requests.get") as mock_get:
        mock_response = mock.Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": 100.0}
        mock_get.return_value = mock_response
        result = convert_currency(100, "USD")
        # Проверяем результат
        assert result == 100.0


def test_fin_transaction_file_not_found(mock_path):
    """Тест отсутствия файла."""
    # Патчим существование файла
    with patch.object(Path, "exists", return_value=False):
        # Вызываем функцию
        result = fin_transaction(mock_path)
    # Проверяем результат
    assert result == {}


def test_fin_transaction_success(mock_path):
    """Тест успешного парсинга JSON-файла."""
    # Мокируем содержимое файла
    mock_data = '{"key": "value"}'
    m = mock_open(read_data=mock_data)
    with patch("builtins.open", m):
        result = fin_transaction(mock_path)
    assert result == {"key": "value"}


def test_file_path_exel(mock_pandas_read_excel):
    """Тестирует успешное чтение Excel файла"""
    from src.reader_csv_exel_file import file_path_exel

    expected_output = [
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 3, "state": "PENDING", "date": "2018-09-12T21:27:25.241689"},
    ]
    result = file_path_exel("../data/transactions_excel.xlsx")
    assert result == expected_output
    mock_pandas_read_excel.assert_called_once_with("../data/transactions_excel.xlsx")


def test_file_not_found():
    """Тестирует обработку отсутствующего файла"""
    from src.reader_csv_exel_file import file_path_exel

    with pytest.raises(FileNotFoundError):
        file_path_exel("/path/to/nonexistent/file.xlsx")


def test_general_exception_handling():
    """Тестирует общую обработку исключений"""
    from src.reader_csv_exel_file import file_path_exel

    with patch("your_module.pd.read_excel", side_effect=Exception("Test exception")):
        result = file_path_exel("../data/transactions_excel.xlsx")
        assert result is None


# Фикстуры для теста CSV
@pytest.fixture
def mock_csv_file():
    """Фиктивное содержание CSV файла"""
    content = b"id;state;date\n1;EXECUTED;2019-07-03T18:35:29.512364"
    return mock_open(read_data=content.decode("utf-8"))


# Фикстуры для теста Excel
@pytest.fixture
def mock_excel_file():
    """Фиктивные данные для Excel файла"""
    mock_df = pd.DataFrame(
        {
            "id": [1, 2, 3],
            "state": ["EXECUTED", "CANCELED", "PENDING"],
            "date": ["2019-07-03T18:35:29.512364", "2018-10-14T08:21:33.419441", "2018-09-12T21:27:25.241689"],
        }
    )
    return mock_df


# Тесты для функции file_path_csv
def test_file_path_csv(mock_csv_file):
    """Тестирует успешное чтение CSV файла"""
    with mock_csv_file() as m:
        result = file_path_csv("../data/transactionscsv.csv")
        expected_output = [{"id": "1", "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"}]
        assert result == expected_output
        m.assert_called_once_with("../data/transactionscsv.csv", "r", newline="", encoding="utf-8")


def test_file_not_found_csv():
    """Тестирует обработку отсутствующего CSV файла"""
    with pytest.raises(FileNotFoundError):
        file_path_csv("/path/to/nonexistent/file.csv")


def test_general_exception_handling_csv():
    """Тестирует общую обработку исключений при чтении CSV файла"""
    with mock_open() as m:
        m.side_effect = Exception("Test exception")
        result = file_path_csv("../data/transactionscsv.csv")
        assert result is None
        m.assert_called_once_with("../data/transactionscsv.csv", "r", newline="", encoding="utf-8")


# Тесты для функции file_path_exel
def test_file_path_exe(mock_excel_file):
    """Тестирует успешное чтение Excel файла"""
    with patch("pandas.read_excel", return_value=mock_excel_file) as mock_read_excel:
        expected_output = [
            {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
            {"id": 2, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
            {"id": 3, "state": "PENDING", "date": "2018-09-12T21:27:25.241689"},
        ]
        result = file_path_exel("../data/transactions_excel.xlsx")
        assert result == expected_output
        mock_read_excel.assert_called_once_with("../data/transactions_excel.xlsx")


def test_file_not_found_exel():
    """Тестирует обработку отсутствующего Excel файла"""
    with pytest.raises(FileNotFoundError):
        file_path_exel("/path/to/nonexistent/file.xlsx")


def test_general_exception_handling_exel():
    """Тестирует общую обработку исключений при чтении Excel файла"""
    with patch("pandas.read_excel", side_effect=Exception("Test exception")):
        result = file_path_exel("../data/transactions_excel.xlsx")
        assert result is None
