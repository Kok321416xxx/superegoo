''' Импорт нужных функций '''
from src.masks import get_mask_account, get_mask_card_number


def mask_account_card(card_tipe_number: str) -> str:
    ''' Функция спределяет счет или карточка, возвращает соотвествующую кодировку '''
    card_split = card_tipe_number.split()
    if card_split[0] == 'Счет':
        return f"{card_split[0]} {get_mask_account(card_split[-1])}"
    else:
        return f"{card_split[0]} {get_mask_card_number(card_split[-1])}"


def get_date(iso_date_str: str) -> str:
    ''' Функция  принимает на вход строку с датой и возвращает строку с датой в формате ("11.03.2024" ).'''
    date_part = iso_date_str.split('T')[0]
    year, month, day = date_part.split('-')
    result = f"{day}.{month}.{year}"
    return result

