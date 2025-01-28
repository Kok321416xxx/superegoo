def get_mask_card_number(num_card: str) -> str:
    """Принимает на вход номер карты и возвращает ее маску  XXXX XX** **** XXXX"""
    return num_card[0:4] + " " + num_card[5:7] + "**" + " **** " + num_card[-4:]


def get_mask_account(small_num_card: str) -> str:
    """Принимает на вход номер карты и возвращает ее маску **XXXX"""
    return "**" + small_num_card[-4:]

def get_date(day, mounth, year: str) -> str:
    """"Принимает на вход день, месяц, год и возвращает Д.М.Г """
    return day + '.' +mounth + '.' + year


