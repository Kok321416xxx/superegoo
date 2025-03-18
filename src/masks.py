from src.decorators import log


@log("log_test_file")
def get_mask_card_number(num_card: str) -> str:
    if len(num_card) != 16:
        raise ValueError("Некорректная длинна номера")
    """Принимает на вход номер карты и возвращает ее маску  XXXX XX** **** XXXX"""
    return num_card[0:4] + " " + num_card[4:6] + "**" + " **** " + num_card[-4:]


def get_mask_account(small_num_card: str) -> str:
    if len(small_num_card) != 20:
        raise ValueError("Некорректная длинна номера счета")
    """Принимает на вход номер карты и возвращает ее маску **XXXX"""
    return "**" + small_num_card[-4:]
