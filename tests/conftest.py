import pytest


@pytest.fixture
def fixture_get_mask_card_number():
    return [("1234567890123456", "1234 56** **** 3456")]

@pytest.fixture
def fixture_get_mask_account():
    return [("73654108430135874305", "**4305")]

@pytest.fixture
def sample_data():
    return [
        {'id': 41428829, 'state': 'EXECUTED', 'date': '2019-07-03T18:35:29.512364'},
        {'id': 939719570, 'state': 'EXECUTED', 'date': '2018-06-30T02:08:58.425572'},
        {'id': 594226727, 'state': 'CANCELED', 'date': '2018-09-12T21:27:25.241689'},
        {'id': 615064591, 'state': 'CANCELED', 'date': '2018-10-14T08:21:33.419441'}
    ]
